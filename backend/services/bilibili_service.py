"""
BENserviceEN - EN
ENbilitoolEN，useENAPIcall
"""

import asyncio
import json
import logging
import os
import hashlib
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any
from uuid import UUID

import aiofiles
import aiohttp
from sqlalchemy.orm import Session

from ..models.bilibili import BilibiliAccount, UploadRecord
from ..schemas.bilibili import BilibiliAccountCreate, UploadRequest
from ..utils.crypto import encrypt_data, decrypt_data

logger = logging.getLogger(__name__)


class BilibiliAccountService:
    """BENaccountservice"""
    
    def __init__(self, db: Session):
        self.db = db
    
    async def verify_cookie(self, cookie: str) -> Tuple[bool, Optional[Dict]]:
        """validateBENCookieEN"""
        try:
            headers = {
                "Cookie": cookie,
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "Referer": "https://www.bilibili.com/"
            }
            
            async with aiohttp.ClientSession() as session:
                # ENcheckloginstatus
                async with session.get(
                    "https://api.bilibili.com/x/web-interface/nav",
                    headers=headers,
                    timeout=aiohttp.ClientTimeout(total=10)
                ) as response:
                    data = await response.json()
                    
                    if data.get("code") == 0 and data.get("data", {}).get("isLogin"):
                        user_info = data["data"]
                        
                        return True, {
                            "uid": user_info.get("mid"),
                            "username": user_info.get("uname"),
                            "face": user_info.get("face"),
                            "level": user_info.get("level_info", {}).get("current_level", 0),
                            "can_upload": True,  # ENTrue，ENAPIcall
                            "vip_status": user_info.get("vipStatus", 0),
                            "verified_at": datetime.now().isoformat()
                        }
                    else:
                        logger.warning(f"Cookievalidatefailed: code={data.get('code')}, message={data.get('message')}")
                        return False, None
                        
        except asyncio.TimeoutError:
            logger.error("validateCookietimeout")
            return False, None
        except Exception as e:
            logger.error(f"validateCookiefailed: {e}")
            return False, None
    
    async def create_account(self, account_data: BilibiliAccountCreate) -> BilibiliAccount:
        """createBENaccount"""
        try:
            # validateCookie
            is_valid, user_info = await self.verify_cookie(account_data.cookie_content)
            if not is_valid:
                raise ValueError("ENCookie，pleasecheckCookieEN")
            
            # checkaccountENalready exists
            existing_account = self.db.query(BilibiliAccount).filter(
                BilibiliAccount.username == user_info.get("username")
            ).first()
            
            if existing_account:
                # updateENaccountEN
                existing_account.cookies = encrypt_data(account_data.cookie_content)
                existing_account.nickname = account_data.nickname or user_info.get("username")
                existing_account.status = "active"
                existing_account.updated_at = datetime.now()
                
                self.db.commit()
                self.db.refresh(existing_account)
                
                logger.info(f"updateENBENaccount: {existing_account.username}")
                return existing_account
            
            # ENcookies
            encrypted_cookies = encrypt_data(account_data.cookie_content)
            
            # createENaccountEN
            account = BilibiliAccount(
                username=user_info.get("username", account_data.username),
                nickname=account_data.nickname or user_info.get("username", "BENuser"),
                cookies=encrypted_cookies,
                status="active",
                created_at=datetime.now(),
                updated_at=datetime.now()
            )
            
            self.db.add(account)
            self.db.commit()
            self.db.refresh(account)
            
            logger.info(f"BENaccountcreatesucceeded: {account.username} (UID: {user_info.get('uid')})")
            return account
            
        except Exception as e:
            self.db.rollback()
            logger.error(f"createBENaccountfailed: {e}")
            raise
    
    async def check_account_health(self, account_id: int) -> Dict[str, Any]:
        """checkaccountENstatus"""
        try:
            account = self.db.query(BilibiliAccount).filter(
                BilibiliAccount.id == account_id
            ).first()
            
            if not account:
                raise ValueError("accountdoes not exist")
            
            # ENCookie
            decrypted_cookies = decrypt_data(account.cookies)
            
            # validateCookieEN
            is_valid, user_info = await self.verify_cookie(decrypted_cookies)
            
            health_status = {
                "account_id": account_id,
                "username": account.username,
                "is_valid": is_valid,
                "checked_at": datetime.now().isoformat(),
                "last_verified": account.updated_at.isoformat() if account.updated_at else None
            }
            
            if is_valid and user_info:
                health_status.update({
                    "user_info": user_info,
                    "can_upload": user_info.get("can_upload", False),
                    "level": user_info.get("level", 0),
                    "vip_status": user_info.get("vip_status", 0)
                })
                
                # updateaccountstatus
                account.status = "active"
                account.updated_at = datetime.now()
            else:
                health_status["error"] = "CookieENaccountexception"
                account.status = "inactive"
            
            self.db.commit()
            return health_status
            
        except Exception as e:
            logger.error(f"checkaccountENstatusfailed: {e}")
            return {
                "account_id": account_id,
                "is_valid": False,
                "error": str(e),
                "checked_at": datetime.now().isoformat()
            }
    
    async def batch_check_accounts_health(self) -> List[Dict[str, Any]]:
        """ENcheckallaccountENstatus"""
        try:
            accounts = self.db.query(BilibiliAccount).all()
            results = []
            
            for account in accounts:
                health_status = await self.check_account_health(account.id)
                results.append(health_status)
                
                # ENrequestEN
                await asyncio.sleep(1)
            
            logger.info(f"ENcheckEN，ENcheck {len(results)} ENaccount")
            return results
            
        except Exception as e:
            logger.error(f"ENcheckaccountENstatusfailed: {e}")
            raise
    
    def get_active_accounts(self) -> List[BilibiliAccount]:
        """fetchallENaccount"""
        try:
            accounts = self.db.query(BilibiliAccount).filter(
                BilibiliAccount.status == "active"
            ).order_by(BilibiliAccount.updated_at.desc()).all()
            
            return accounts
            
        except Exception as e:
            logger.error(f"fetchENaccountfailed: {e}")
            return []
    
    def get_account_by_id(self, account_id: int) -> Optional[BilibiliAccount]:
        """ENIDfetchaccount"""
        try:
            return self.db.query(BilibiliAccount).filter(
                BilibiliAccount.id == account_id
            ).first()
            
        except Exception as e:
            logger.error(f"fetchaccountfailed: {e}")
            return None
    
    def select_best_account(self, exclude_ids: List[int] = None) -> Optional[BilibiliAccount]:
        """ENuploadaccount"""
        try:
            query = self.db.query(BilibiliAccount).filter(
                BilibiliAccount.status == "active"
            )
            
            if exclude_ids:
                query = query.filter(~BilibiliAccount.id.in_(exclude_ids))
            
            accounts = query.all()
            
            if not accounts:
                return None
            
            # EN：VIP > EN > ENusetime
            def account_priority(account):
                # VIPaccountEN
                vip_score = account.vip_status * 1000 if hasattr(account, 'vip_status') else 0
                # EN
                level_score = getattr(account, 'level', 0) * 100
                # ENusetime（ENuseEN）
                last_used = account.updated_at or account.created_at
                time_score = (datetime.now() - last_used).total_seconds() / 3600  # EN
                
                return vip_score + level_score + time_score
            
            best_account = max(accounts, key=account_priority)
            logger.info(f"ENaccountENupload: {best_account.username} (ID: {best_account.id})")
            
            return best_account
            
        except Exception as e:
            logger.error(f"ENaccountfailed: {e}")
            return None
    
    def get_account_upload_stats(self, account_id: int, days: int = 7) -> Dict[str, Any]:
        """fetchaccountuploadEN"""
        try:
            from datetime import timedelta
            
            start_date = datetime.now() - timedelta(days=days)
            
            # ENuploadEN
            upload_records = self.db.query(UploadRecord).filter(
                UploadRecord.account_id == account_id,
                UploadRecord.created_at >= start_date
            ).all()
            
            total_uploads = len(upload_records)
            successful_uploads = len([r for r in upload_records if r.status == 'success'])
            failed_uploads = len([r for r in upload_records if r.status == 'failed'])
            
            success_rate = (successful_uploads / total_uploads * 100) if total_uploads > 0 else 0
            
            return {
                "account_id": account_id,
                "days": days,
                "total_uploads": total_uploads,
                "successful_uploads": successful_uploads,
                "failed_uploads": failed_uploads,
                "success_rate": round(success_rate, 2),
                "last_upload": upload_records[-1].created_at.isoformat() if upload_records else None
            }
            
        except Exception as e:
            logger.error(f"fetchaccountENfailed: {e}")
            return {
                "account_id": account_id,
                "error": str(e)
            }
    
    def rotate_accounts_for_batch_upload(self, video_count: int) -> List[BilibiliAccount]:
        """ENuploadENaccount（EN）"""
        try:
            active_accounts = self.get_active_accounts()
            
            if not active_accounts:
                return []
            
            # ifvideoENaccountEN，EN
            if video_count <= len(active_accounts):
                return active_accounts[:video_count]
            
            # elseEN
            allocated_accounts = []
            for i in range(video_count):
                account_index = i % len(active_accounts)
                allocated_accounts.append(active_accounts[account_index])
            
            logger.info(f"EN {video_count} ENvideoEN {len(set(allocated_accounts))} ENaccount")
            return allocated_accounts
            
        except Exception as e:
            logger.error(f"accountENfailed: {e}")
            return []
    
    def update_account_usage(self, account_id: int):
        """updateaccountusetime"""
        try:
            account = self.get_account_by_id(account_id)
            if account:
                account.updated_at = datetime.now()
                self.db.commit()
                
        except Exception as e:
            logger.error(f"updateaccountusetimefailed: {e}")
    
    def get_accounts(self) -> List[BilibiliAccount]:
        """fetchallaccount"""
        return self.db.query(BilibiliAccount).all()
    
    def get_account(self, account_id: UUID) -> Optional[BilibiliAccount]:
        """fetchENaccount"""
        return self.db.query(BilibiliAccount).filter(BilibiliAccount.id == account_id).first()
    
    def delete_account(self, account_id: UUID) -> bool:
        """deleteaccount"""
        account = self.get_account(account_id)
        if not account:
            return False
        
        try:
            # ENdeleteallEN
            from ..models.bilibili import UploadRecord
            upload_records = self.db.query(UploadRecord).filter(UploadRecord.account_id == account_id).all()
            
            for record in upload_records:
                logger.info(f"deleteEN: {record.id}")
                self.db.delete(record)
            
            # deleteaccount
            self.db.delete(account)
            self.db.commit()
            
            logger.info(f"BENaccountdeletesucceeded: {account.username}，meanwhiledeleteEN {len(upload_records)} EN")
            return True
            
        except Exception as e:
            self.db.rollback()
            logger.error(f"deleteaccountfailed: {str(e)}")
            return False
    
    def check_account_status(self, account_id: UUID) -> bool:
        """checkaccountstatus"""
        account = self.get_account(account_id)
        if not account:
            return False
        
        try:
            # ENcookies
            try:
                cookies_data_str = decrypt_data(account.cookies)
                # validatecookieEN
                if not cookies_data_str or not isinstance(cookies_data_str, str):
                    return False
                return True
            except Exception as e:
                logger.warning(f"ENcookiesfailed: {str(e)}")
                return False
                    
        except Exception as e:
            logger.error(f"checkaccountstatusfailed: {str(e)}")
            return False


class BilibiliUploadService:
    """BENservice - useENAPIcall"""
    
    def __init__(self, db: Session):
        self.db = db
        self.account_service = BilibiliAccountService(db)
    
    def create_upload_record(self, project_id: UUID, upload_data: UploadRequest) -> UploadRecord:
        """createEN"""
        # validateaccount
        account = self.account_service.get_account(upload_data.account_id)
        if not account:
            raise ValueError("accountdoes not exist")
        
        # createEN
        record = UploadRecord(
            project_id=project_id,
            account_id=upload_data.account_id,
            clip_id=",".join(upload_data.clip_ids),  # EN
            title=upload_data.title,
            description=upload_data.description,
            tags=json.dumps(upload_data.tags),
            partition_id=upload_data.partition_id,
            status="pending"
        )
        
        self.db.add(record)
        self.db.commit()
        self.db.refresh(record)
        
        logger.info(f"ENcreatesucceeded: {record.id}")
        return record
    
    async def upload_clip(self, record_id: int, video_path: str, max_retries: int = 3) -> bool:
        """uploadENclip - useENuploadEN"""
        try:
            # fetchEN
            record = self.db.query(UploadRecord).filter(UploadRecord.id == record_id).first()
            if not record:
                logger.error(f"ENdoes not exist: {record_id}")
                return False
            
            # fetchaccountEN
            account = self.db.query(BilibiliAccount).filter(BilibiliAccount.id == record.account_id).first()
            if not account:
                logger.error(f"accountdoes not exist: {record.account_id}")
                return False
            
            # ENCookie
            cookies = decrypt_data(account.cookies)
            if not cookies:
                logger.error("CookieENfailed")
                return False
            
            # useENuploadEN
            uploader = BilibiliDirectUploader(cookies)
            success = await uploader.upload_video(
                video_path=video_path,
                metadata={
                    'title': record.title,
                    'desc': record.description or '',
                    'tid': record.tid,
                    'tag': record.tags or '',
                    'source': record.source or '',
                    'copyright': record.copyright or 1
                },
                max_retries=max_retries
            )
            
            if success:
                record.status = 'completed'
                record.bv_id = uploader.bv_id
                record.completed_at = datetime.utcnow()
            else:
                record.status = 'failed'
                record.error_message = uploader.error_message
                record.failed_at = datetime.utcnow()
            
            self.db.commit()
            return success
            
        except Exception as e:
            logger.error(f"uploadclipfailed: {e}")
            # updateENstatus
            try:
                record = self.db.query(UploadRecord).filter(UploadRecord.id == record_id).first()
                if record:
                    record.status = 'failed'
                    record.error_message = str(e)
                    record.failed_at = datetime.utcnow()
                    self.db.commit()
            except:
                pass
            return False
    
    def update_upload_status(self, record_id, status: str, error_message: str = None) -> bool:
        """updateENstatus"""
        try:
            record = self.db.query(UploadRecord).filter(UploadRecord.id == record_id).first()
            if not record:
                return False
            
            record.status = status
            if error_message:
                record.error_message = error_message
            record.updated_at = datetime.utcnow()
            
            self.db.commit()
            return True
        except Exception as e:
            logger.error(f"updateENstatusfailed: {str(e)}")
            self.db.rollback()
            return False

    def retry_upload_task(self, record_id: int) -> bool:
        """retryfailedENtask"""
        try:
            record = self.db.query(UploadRecord).filter(UploadRecord.id == record_id).first()
            if not record:
                raise ValueError("ENdoes not exist")
            
            if record.status != "failed":
                raise ValueError("ENfailedENtaskcanretry")
            
            # ENstatusENprocessing
            record.status = "pending"
            record.error_message = None
            record.updated_at = datetime.utcnow()
            self.db.commit()
            
            # ENstartuploadtask
            clip_ids = record.clip_id.split(",") if record.clip_id else []
            for clip_id in clip_ids:
                clip_id = clip_id.strip()
                if clip_id:
                    from ..tasks.upload import upload_clip_task
                    upload_clip_task.delay(str(record.id), clip_id)
            
            logger.info(f"ENtaskretryENstart: {record_id}")
            return True
            
        except Exception as e:
            logger.error(f"retryENtaskfailed: {str(e)}")
            self.db.rollback()
            return False

    def cancel_upload_task(self, record_id: int) -> bool:
        """cancelENtask"""
        try:
            record = self.db.query(UploadRecord).filter(UploadRecord.id == record_id).first()
            if not record:
                raise ValueError("ENdoes not exist")
            
            if record.status not in ["pending", "processing"]:
                raise ValueError("ENprocessingENprocessingENtaskcancancel")
            
            # updatestatusENcancel
            record.status = "cancelled"
            record.updated_at = datetime.utcnow()
            self.db.commit()
            
            logger.info(f"ENtaskENcancel: {record_id}")
            return True
            
        except Exception as e:
            logger.error(f"cancelENtaskfailed: {str(e)}")
            self.db.rollback()
            return False
    
    def delete_upload_task(self, record_id: int) -> bool:
        """deleteENtask"""
        try:
            record = self.db.query(UploadRecord).filter(UploadRecord.id == record_id).first()
            if not record:
                raise ValueError("ENdoes not exist")
            
            # ENcompleted、failedENcancelENtaskcandelete
            if record.status in ["pending", "processing"]:
                raise ValueError("ENtaskENdelete，pleaseENcancel")
            
            # deleteEN
            self.db.delete(record)
            self.db.commit()
            
            logger.info(f"ENtaskdeleted: {record_id}")
            return True
            
        except Exception as e:
            logger.error(f"deleteENtaskfailed: {str(e)}")
            self.db.rollback()
            return False
    
    def get_upload_records(self, project_id: Optional[UUID] = None) -> List[dict]:
        """fetchEN，EN"""
        from ..models.project import Project
        
        query = self.db.query(
            UploadRecord,
            BilibiliAccount.username.label('account_username'),
            BilibiliAccount.nickname.label('account_nickname'),
            Project.name.label('project_name')
        ).join(
            BilibiliAccount, UploadRecord.account_id == BilibiliAccount.id
        ).outerjoin(
            Project, UploadRecord.project_id == Project.id
        )
        
        if project_id:
            query = query.filter(UploadRecord.project_id == project_id)
        
        results = query.order_by(UploadRecord.created_at.desc()).all()
        
        # EN，EN
        records = []
        for record, account_username, account_nickname, project_name in results:
            record_dict = {
                'id': record.id,
                'task_id': record.task_id,
                'project_id': record.project_id,
                'account_id': record.account_id,
                'clip_id': record.clip_id,
                'title': record.title,
                'description': record.description,
                'tags': record.tags,
                'partition_id': record.partition_id,
                'video_path': record.video_path,
                'bv_id': record.bv_id,
                'av_id': record.av_id,
                'status': record.status,
                'error_message': record.error_message,
                'progress': record.progress or 0,
                'file_size': record.file_size,
                'upload_duration': record.upload_duration,
                'created_at': record.created_at,
                'updated_at': record.updated_at,
                'account_username': account_username,
                'account_nickname': account_nickname,
                'project_name': project_name
            }
            records.append(record_dict)
        
        return records
    
    def get_upload_record(self, record_id: UUID) -> Optional[UploadRecord]:
        """fetchEN"""
        return self.db.query(UploadRecord).filter(UploadRecord.id == record_id).first()
    
    def get_upload_record_by_id(self, record_id: int) -> Optional[UploadRecord]:
        """ENIDfetchEN"""
        return self.db.query(UploadRecord).filter(UploadRecord.id == record_id).first()
    
    def upload_clip_sync(self, record_id: int, video_path: str, max_retries: int = 3) -> bool:
        """ENuploadENclip"""
        try:
            # fetchEN
            record = self.db.query(UploadRecord).filter(UploadRecord.id == record_id).first()
            if not record:
                logger.error(f"ENdoes not exist: {record_id}")
                return False
            
            # fetchaccountEN
            account = self.db.query(BilibiliAccount).filter(BilibiliAccount.id == record.account_id).first()
            if not account:
                logger.error(f"accountdoes not exist: {record.account_id}")
                return False
            
            # ENCookie
            cookies = decrypt_data(account.cookies)
            if not cookies:
                logger.error("CookieENfailed")
                return False
            
            # useENuploadEN（EN）
            uploader = BilibiliDirectUploader(cookies)
            success = uploader.upload_video_sync(
                video_path=video_path,
                metadata={
                    'title': record.title,
                    'desc': record.description or '',
                    'tid': record.tid,
                    'tag': record.tags or '',
                    'source': record.source or '',
                    'copyright': record.copyright or 1
                },
                max_retries=max_retries
            )
            
            if success:
                record.status = 'completed'
                record.bv_id = uploader.bv_id
                record.completed_at = datetime.utcnow()
            else:
                record.status = 'failed'
                record.error_message = uploader.error_message
                record.failed_at = datetime.utcnow()
            
            self.db.commit()
            return success
            
        except Exception as e:
            logger.error(f"uploadclipfailed: {e}")
            # updateENstatus
            try:
                record = self.db.query(UploadRecord).filter(UploadRecord.id == record_id).first()
                if record:
                    record.status = 'failed'
                    record.error_message = str(e)
                    record.failed_at = datetime.utcnow()
                    self.db.commit()
            except:
                pass
            return False


class BilibiliDirectUploader:
    """BENAPIuploadEN"""
    
    def __init__(self, cookies: str):
        self.cookies = cookies
        self.bv_id = None
        self.error_message = None
        self.session = None
    
    async def upload_video(self, video_path: str, metadata: dict, max_retries: int = 3) -> bool:
        """uploadvideo - EN，ENreturnfailedstatus"""
        try:
            # ENreturnfailed，becauseneedENuploadEN
            self.error_message = "uploadENcurrentlyEN，pleaseEN"
            logger.warning("uploadEN，returnfailedstatus")
            return False
                
        except Exception as e:
            self.error_message = str(e)
            logger.error(f"uploadvideofailed: {e}")
            return False
    
    def upload_video_sync(self, video_path: str, metadata: dict, max_retries: int = 3) -> bool:
        """ENuploadvideo"""
        try:
            # ENreturnfailed，becauseneedENuploadEN
            self.error_message = "uploadENcurrentlyEN，pleaseEN"
            logger.warning("uploadEN，returnfailedstatus")
            return False
                
        except Exception as e:
            self.error_message = str(e)
            logger.error(f"uploadvideofailed: {e}")
            return False
    
    async def _pre_upload(self, video_path: str) -> Optional[str]:
        """ENupload，fetchupload_id"""
        try:
            file_size = os.path.getsize(video_path)
            file_name = os.path.basename(video_path)
            
            headers = {
                "Cookie": self.cookies,
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                "Referer": "https://member.bilibili.com/"
            }
            
            data = {
                "name": file_name,
                "size": str(file_size)
            }
            
            async with self.session.post(
                "https://member.bilibili.com/x/vu/web/add",
                headers=headers,
                data=data,
                timeout=aiohttp.ClientTimeout(total=30)
            ) as response:
                result = await response.json()
                
                if result.get("code") == 0:
                    upload_id = result.get("data", {}).get("id")
                    logger.info(f"ENuploadsucceeded，upload_id: {upload_id}")
                    return upload_id
                else:
                    self.error_message = f"ENuploadfailed: {result.get('message', 'Unknown error')}"
                    logger.error(self.error_message)
                    return None
                    
        except Exception as e:
            self.error_message = f"ENuploadexception: {str(e)}"
            logger.error(self.error_message)
            return None
    
    async def _chunk_upload(self, video_path: str, upload_id: str, max_retries: int = 3) -> bool:
        """ENupload"""
        try:
            chunk_size = 2 * 1024 * 1024  # 2MB per chunk
            file_size = os.path.getsize(video_path)
            
            headers = {
                "Cookie": self.cookies,
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                "Referer": "https://member.bilibili.com/"
            }
            
            with open(video_path, 'rb') as f:
                chunk_index = 0
                while True:
                    chunk_data = f.read(chunk_size)
                    if not chunk_data:
                        break
                    
                    # retryEN
                    for attempt in range(max_retries):
                        try:
                            form_data = aiohttp.FormData()
                            form_data.add_field('chunk', chunk_data, filename=f'chunk_{chunk_index}')
                            form_data.add_field('id', upload_id)
                            form_data.add_field('chunk_index', str(chunk_index))
                            
                            async with self.session.post(
                                "https://member.bilibili.com/x/vu/web/upload",
                                headers=headers,
                                data=form_data,
                                timeout=aiohttp.ClientTimeout(total=60)
                            ) as response:
                                result = await response.json()
                                
                                if result.get("code") == 0:
                                    logger.info(f"EN {chunk_index} uploadsucceeded")
                                    break
                                else:
                                    if attempt == max_retries - 1:
                                        self.error_message = f"EN {chunk_index} uploadfailed: {result.get('message', 'Unknown error')}"
                                        logger.error(self.error_message)
                                        return False
                                    else:
                                        await asyncio.sleep(2 ** attempt)
                                        
                        except Exception as e:
                            if attempt == max_retries - 1:
                                self.error_message = f"EN {chunk_index} uploadexception: {str(e)}"
                                logger.error(self.error_message)
                                return False
                            else:
                                await asyncio.sleep(2 ** attempt)
                    
                    chunk_index += 1
            
            logger.info(f"allENuploadEN，EN {chunk_index} EN")
            return True
            
        except Exception as e:
            self.error_message = f"ENuploadexception: {str(e)}"
            logger.error(self.error_message)
            return False
    
    async def _merge_chunks(self, upload_id: str) -> bool:
        """EN"""
        try:
            headers = {
                "Cookie": self.cookies,
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                "Referer": "https://member.bilibili.com/"
            }
            
            data = {
                "id": upload_id
            }
            
            async with self.session.post(
                "https://member.bilibili.com/x/vu/web/merge",
                headers=headers,
                data=data,
                timeout=aiohttp.ClientTimeout(total=120)
            ) as response:
                result = await response.json()
                
                if result.get("code") == 0:
                    logger.info("ENsucceeded")
                    return True
                else:
                    self.error_message = f"ENfailed: {result.get('message', 'Unknown error')}"
                    logger.error(self.error_message)
                    return False
                    
        except Exception as e:
            self.error_message = f"ENexception: {str(e)}"
            logger.error(self.error_message)
            return False
    
    async def _submit_video(self, upload_id: str, metadata: dict) -> bool:
        """EN"""
        try:
            headers = {
                "Cookie": self.cookies,
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                "Referer": "https://member.bilibili.com/",
                "Content-Type": "application/json"
            }
            
            # EN
            submit_data = {
                "copyright": 1,  # EN
                "videos": [{
                    "filename": upload_id,
                    "title": metadata.get('title', ''),
                    "desc": metadata.get('description', '')
                }],
                "source": "",
                "tid": metadata.get('partition_id', 17),
                "cover": "",
                "title": metadata.get('title', ''),
                "tag": ",".join(metadata.get('tags', [])),
                "desc_format_id": 0,
                "desc": metadata.get('description', ''),
                "dynamic": "",
                "subtitle": {
                    "open": 0,
                    "lan": ""
                },
                "open_elec": 0,
                "no_reprint": 0,
                "up_selection_reply": False,
                "up_close_reply": False,
                "up_close_danmu": False
            }
            
            async with self.session.post(
                "https://member.bilibili.com/x/vu/web/add",
                headers=headers,
                json=submit_data,
                timeout=aiohttp.ClientTimeout(total=60)
            ) as response:
                result = await response.json()
                
                if result.get("code") == 0:
                    self.bv_id = result.get("data", {}).get("bvid")
                    logger.info(f"ENsucceeded，BVEN: {self.bv_id}")
                    return True
                else:
                    self.error_message = f"ENfailed: {result.get('message', 'Unknown error')}"
                    logger.error(self.error_message)
                    return False
                    
        except Exception as e:
            self.error_message = f"ENexception: {str(e)}"
            logger.error(self.error_message)
            return False
    
    def get_bv_id(self) -> Optional[str]:
        """fetchBVEN"""
        return self.bv_id
    
    def get_error_message(self) -> Optional[str]:
        """fetcherrorEN"""
        return self.error_message
