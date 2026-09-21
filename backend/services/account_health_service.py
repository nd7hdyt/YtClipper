from typing import Dict, List, Optional, Tuple
import asyncio
import logging
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import select

from ..core.database import get_db
from ..models.bilibili import BilibiliAccount
from ..utils.crypto import decrypt_data, encrypt_data
from ..core.celery_app import celery_app

logger = logging.getLogger(__name__)

class AccountHealthStatus:
    """accountENstatusEN"""
    HEALTHY = "healthy"
    WARNING = "warning"
    CRITICAL = "critical"
    EXPIRED = "expired"
    UNKNOWN = "unknown"

class AccountHealthService:
    """accountENcheckservice"""
    
    def __init__(self):
        self.check_interval = 300  # 5ENcheckEN
        self.cookie_expire_days = 30  # CookieEN
        self.warning_days = 7  # ENwarningEN
        
    async def check_account_health(self, account_id: int) -> Dict:
        """checkENaccountENstatus"""
        try:
            db = next(get_db())
            account = db.query(BilibiliAccount).filter(BilibiliAccount.id == account_id).first()
            
            if not account:
                return {
                    "account_id": account_id,
                    "status": AccountHealthStatus.UNKNOWN,
                    "message": "accountdoes not exist",
                    "last_check": datetime.now()
                }
            
            # checkCookieEN
            cookie_status = await self._check_cookie_validity(account)
            
            # checkloginstatus
            login_status = await self._check_login_status(account)
            
            # checkuploadEN
            upload_status = await self._check_upload_permission(account)
            
            # ENstatus
            overall_status = self._evaluate_overall_status(
                cookie_status, login_status, upload_status
            )
            
            # updateaccountstatus
            account.health_status = overall_status["status"]
            account.last_health_check = datetime.now()
            account.health_details = {
                "cookie": cookie_status,
                "login": login_status,
                "upload": upload_status,
                "last_check": datetime.now().isoformat()
            }
            
            db.commit()
            
            return {
                "account_id": account_id,
                "username": account.username,
                "status": overall_status["status"],
                "message": overall_status["message"],
                "details": {
                    "cookie": cookie_status,
                    "login": login_status,
                    "upload": upload_status
                },
                "last_check": datetime.now()
            }
            
        except Exception as e:
            logger.error(f"checkaccount {account_id} ENstatusfailed: {str(e)}")
            return {
                "account_id": account_id,
                "status": AccountHealthStatus.UNKNOWN,
                "message": f"checkfailed: {str(e)}",
                "last_check": datetime.now()
            }
    
    async def _check_cookie_validity(self, account: BilibiliAccount) -> Dict:
        """checkCookieEN"""
        try:
            if not account.cookies:
                return {
                    "status": AccountHealthStatus.CRITICAL,
                    "message": "CookieEN",
                    "expires_in": None
                }
            
            # ENCookie
            try:
                cookies = decrypt_data(account.cookies)
            except Exception as e:
                return {
                    "status": AccountHealthStatus.CRITICAL,
                    "message": f"CookieENfailed: {str(e)}",
                    "expires_in": None
                }
            
            # checkCookieEN
            required_fields = ['SESSDATA', 'bili_jct', 'DedeUserID']
            missing_fields = []
            
            for field in required_fields:
                if field not in cookies:
                    missing_fields.append(field)
            
            if missing_fields:
                return {
                    "status": AccountHealthStatus.CRITICAL,
                    "message": f"CookieEN: {', '.join(missing_fields)}",
                    "expires_in": None
                }
            
            # checkCookieEN
            if account.cookie_expires_at:
                now = datetime.now()
                expires_in = (account.cookie_expires_at - now).days
                
                if expires_in <= 0:
                    return {
                        "status": AccountHealthStatus.EXPIRED,
                        "message": "CookieEN",
                        "expires_in": expires_in
                    }
                elif expires_in <= self.warning_days:
                    return {
                        "status": AccountHealthStatus.WARNING,
                        "message": f"CookieEN {expires_in} EN",
                        "expires_in": expires_in
                    }
                else:
                    return {
                        "status": AccountHealthStatus.HEALTHY,
                        "message": "CookieEN",
                        "expires_in": expires_in
                    }
            
            return {
                "status": AccountHealthStatus.HEALTHY,
                "message": "CookieEN",
                "expires_in": None
            }
            
        except Exception as e:
            logger.error(f"checkCookieENfailed: {str(e)}")
            return {
                "status": AccountHealthStatus.UNKNOWN,
                "message": f"checkfailed: {str(e)}",
                "expires_in": None
            }
    
    async def _check_login_status(self, account: BilibiliAccount) -> Dict:
        """checkloginstatus"""
        try:
            import aiohttp
            
            if not account.cookies:
                return {
                    "status": AccountHealthStatus.CRITICAL,
                    "message": "ENCookieEN"
                }
            
            # ENCookie
            cookies = decrypt_data(account.cookies)
            
            # ENCookieEN
            cookie_str = '; '.join([f"{k}={v}" for k, v in cookies.items()])
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'Cookie': cookie_str,
                'Referer': 'https://www.bilibili.com/'
            }
            
            # checkloginstatus
            async with aiohttp.ClientSession() as session:
                async with session.get('https://api.bilibili.com/x/web-interface/nav', headers=headers) as response:
                    if response.status == 200:
                        data = await response.json()
                        if data.get('code') == 0:
                            user_info = data.get('data', {})
                            if user_info.get('isLogin'):
                                return {
                                    "status": AccountHealthStatus.HEALTHY,
                                    "message": "loginstatusEN",
                                    "user_info": {
                                        "uname": user_info.get('uname'),
                                        "mid": user_info.get('mid'),
                                        "level": user_info.get('level_info', {}).get('current_level')
                                    }
                                }
                            else:
                                return {
                                    "status": AccountHealthStatus.CRITICAL,
                                    "message": "ENloginstatus"
                                }
                        else:
                            return {
                                "status": AccountHealthStatus.CRITICAL,
                                "message": f"APIreturnerror: {data.get('message')}"
                            }
                    else:
                        return {
                            "status": AccountHealthStatus.CRITICAL,
                            "message": f"requestfailed: HTTP {response.status}"
                        }
            
        except Exception as e:
            logger.error(f"checkloginstatusfailed: {str(e)}")
            return {
                "status": AccountHealthStatus.UNKNOWN,
                "message": f"checkfailed: {str(e)}"
            }
    
    async def _check_upload_permission(self, account: BilibiliAccount) -> Dict:
        """checkuploadEN"""
        try:
            import aiohttp
            
            if not account.cookies:
                return {
                    "status": AccountHealthStatus.CRITICAL,
                    "message": "ENCookieEN"
                }
            
            # ENCookie
            cookies = decrypt_data(account.cookies)
            
            # ENCookieEN
            cookie_str = '; '.join([f"{k}={v}" for k, v in cookies.items()])
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'Cookie': cookie_str,
                'Referer': 'https://member.bilibili.com/'
            }
            
            # checkuploadEN
            async with aiohttp.ClientSession() as session:
                async with session.get('https://member.bilibili.com/x/web/archive/pre', headers=headers) as response:
                    if response.status == 200:
                        data = await response.json()
                        if data.get('code') == 0:
                            return {
                                "status": AccountHealthStatus.HEALTHY,
                                "message": "ENuploadEN"
                            }
                        elif data.get('code') == -101:
                            return {
                                "status": AccountHealthStatus.CRITICAL,
                                "message": "accountENloginENCookieEN"
                            }
                        else:
                            return {
                                "status": AccountHealthStatus.WARNING,
                                "message": f"uploadEN: {data.get('message')}"
                            }
                    else:
                        return {
                            "status": AccountHealthStatus.WARNING,
                            "message": f"cannotcheckuploadEN: HTTP {response.status}"
                        }
            
        except Exception as e:
            logger.error(f"checkuploadENfailed: {str(e)}")
            return {
                "status": AccountHealthStatus.UNKNOWN,
                "message": f"checkfailed: {str(e)}"
            }
    
    def _evaluate_overall_status(self, cookie_status: Dict, login_status: Dict, upload_status: Dict) -> Dict:
        """ENaccountENstatus"""
        statuses = [cookie_status["status"], login_status["status"], upload_status["status"]]
        messages = []
        
        # ENallEN
        if cookie_status["status"] != AccountHealthStatus.HEALTHY:
            messages.append(f"Cookie: {cookie_status['message']}")
        if login_status["status"] != AccountHealthStatus.HEALTHY:
            messages.append(f"login: {login_status['message']}")
        if upload_status["status"] != AccountHealthStatus.HEALTHY:
            messages.append(f"upload: {upload_status['message']}")
        
        # ENstatus
        if AccountHealthStatus.CRITICAL in statuses or AccountHealthStatus.EXPIRED in statuses:
            overall_status = AccountHealthStatus.CRITICAL
        elif AccountHealthStatus.WARNING in statuses:
            overall_status = AccountHealthStatus.WARNING
        elif AccountHealthStatus.UNKNOWN in statuses:
            overall_status = AccountHealthStatus.WARNING
        else:
            overall_status = AccountHealthStatus.HEALTHY
        
        if messages:
            message = "; ".join(messages)
        else:
            message = "accountstatusEN"
        
        return {
            "status": overall_status,
            "message": message
        }
    
    async def check_all_accounts(self) -> List[Dict]:
        """checkallaccountENstatus"""
        try:
            db = next(get_db())
            accounts = db.query(BilibiliAccount).filter(BilibiliAccount.is_active == True).all()
            
            results = []
            for account in accounts:
                result = await self.check_account_health(account.id)
                results.append(result)
            
            return results
            
        except Exception as e:
            logger.error(f"ENcheckaccountENstatusfailed: {str(e)}")
            return []
    
    async def auto_refresh_cookies(self, account_id: int) -> Dict:
        """ENCookie"""
        try:
            db = next(get_db())
            account = db.query(BilibiliAccount).filter(BilibiliAccount.id == account_id).first()
            
            if not account:
                return {
                    "success": False,
                    "message": "accountdoes not exist"
                }
            
            # ENcanENCookieEN
            # for examplethroughENlogin、ENvalidateEN
            # ENreturnhintEN
            
            return {
                "success": False,
                "message": "ENCookieEN，pleaseENupdateCookie",
                "account_id": account_id,
                "username": account.username
            }
            
        except Exception as e:
            logger.error(f"ENCookiefailed: {str(e)}")
            return {
                "success": False,
                "message": f"ENfailed: {str(e)}"
            }

# ENserviceEN
health_service = AccountHealthService()

# Celerytask
@celery_app.task(name="check_account_health")
def check_account_health_task(account_id: int):
    """checkaccountENstatusENCelerytask"""
    import asyncio
    
    async def run_check():
        return await health_service.check_account_health(account_id)
    
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        result = loop.run_until_complete(run_check())
        return result
    finally:
        loop.close()

@celery_app.task(name="check_all_accounts_health")
def check_all_accounts_health_task():
    """ENcheckallaccountENstatusENCelerytask"""
    import asyncio
    
    async def run_check():
        return await health_service.check_all_accounts()
    
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        result = loop.run_until_complete(run_check())
        return result
    finally:
        loop.close()

@celery_app.task(name="auto_refresh_cookies")
def auto_refresh_cookies_task(account_id: int):
    """ENCookieENCelerytask"""
    import asyncio
    
    async def run_refresh():
        return await health_service.auto_refresh_cookies(account_id)
    
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        result = loop.run_until_complete(run_refresh())
        return result
    finally:
        loop.close()