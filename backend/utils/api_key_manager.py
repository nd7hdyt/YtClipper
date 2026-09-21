"""
APIENsystem - EN、validateEN
"""
import os
import json
import hashlib
import logging
import tempfile
from pathlib import Path
from typing import Optional, Dict, Any, List
from datetime import datetime, timedelta
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64

from .error_handler import ConfigurationError, APIError, ValidationError

logger = logging.getLogger(__name__)

class APIKeyManager:
    """APIEN"""
    
    def __init__(self, storage_path: Optional[Path] = None, master_password: Optional[str] = None):
        """
        initializeAPIEN
        
        Args:
            storage_path: ENpath
            master_password: EN，EN
        """
        self.storage_path = storage_path or Path.home() / ".auto_clips" / "api_keys"
        self.master_password = master_password or self._get_master_password()
        self.fernet = self._create_fernet()
        self.keys_file = self.storage_path / "keys.enc"
        self.metadata_file = self.storage_path / "metadata.json"
        
        # ENsaveENdirectoryEN
        self.storage_path.mkdir(parents=True, exist_ok=True)
        
        # loadEN
        self._load_keys()
    
    def _get_master_password(self) -> str:
        """fetchEN"""
        # ENfetch
        master_password = os.getenv("AUTO_CLIPS_MASTER_PASSWORD")
        if master_password:
            return master_password
        
        # ifENsettings，useEN（EN）
        if os.getenv("AUTO_CLIPS_DEV_MODE"):
            return "dev_master_password"
        
        # ENshouldsettingsEN
        raise ConfigurationError(
            "ENsettingsEN。pleasesettings AUTO_CLIPS_MASTER_PASSWORD EN。"
        )
    
    def _create_fernet(self) -> Fernet:
        """createFernetEN"""
        # useENgenerateEN
        salt = b'auto_clips_salt'  # ENshoulduseENsalt
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(self.master_password.encode()))
        return Fernet(key)
    
    def _load_keys(self):
        """loadEN"""
        self.keys: Dict[str, Dict[str, Any]] = {}
        
        if self.keys_file.exists():
            try:
                with open(self.keys_file, 'rb') as f:
                    encrypted_data = f.read()
                    decrypted_data = self.fernet.decrypt(encrypted_data)
                    self.keys = json.loads(decrypted_data.decode())
                logger.info(f"succeededload {len(self.keys)} ENAPIEN")
            except Exception as e:
                logger.warning(f"loadAPIENfailed: {e}")
                self.keys = {}
        
        # loadEN
        self.metadata: Dict[str, Any] = {}
        if self.metadata_file.exists():
            try:
                with open(self.metadata_file, 'r', encoding='utf-8') as f:
                    self.metadata = json.load(f)
            except Exception as e:
                logger.warning(f"loadAPIENfailed: {e}")
                self.metadata = {}
    
    def _save_keys(self):
        """saveENfile"""
        try:
            # ENsaveEN
            data = json.dumps(self.keys, ensure_ascii=False)
            encrypted_data = self.fernet.encrypt(data.encode())
            
            with open(self.keys_file, 'wb') as f:
                f.write(encrypted_data)
            
            # saveEN（EN）
            with open(self.metadata_file, 'w', encoding='utf-8') as f:
                json.dump(self.metadata, f, ensure_ascii=False, indent=2)
            
            logger.debug("APIENsave")
        except Exception as e:
            logger.error(f"saveAPIENfailed: {e}")
            raise ConfigurationError(f"saveAPIENfailed: {e}")
    
    def add_api_key(self, key_name: str, api_key: str, provider: str = "dashscope", 
                   description: str = "", expires_at: Optional[datetime] = None) -> bool:
        """
        ENAPIEN
        
        Args:
            key_name: EN
            api_key: APIEN
            provider: EN（ENdashscope）
            description: descriptionEN
            expires_at: ENtime
            
        Returns:
            ENsucceeded
        """
        try:
            # validateEN
            if not self._validate_api_key_format(api_key, provider):
                raise ValidationError(f"EN{provider} APIEN")
            
            # checkENalready exists
            if key_name in self.keys:
                logger.warning(f"EN '{key_name}' already exists，EN")
            
            # EN
            self.keys[key_name] = {
                "api_key": api_key,
                "provider": provider,
                "description": description,
                "created_at": datetime.now().isoformat(),
                "expires_at": expires_at.isoformat() if expires_at else None,
                "last_used": None,
                "usage_count": 0,
                "is_active": True
            }
            
            # updateEN
            self.metadata["last_updated"] = datetime.now().isoformat()
            self.metadata["total_keys"] = len(self.keys)
            
            # saveENfile
            self._save_keys()
            
            logger.info(f"succeededENAPIEN: {key_name}")
            return True
            
        except Exception as e:
            logger.error(f"ENAPIENfailed: {e}")
            raise
    
    def get_api_key(self, key_name: str) -> Optional[str]:
        """
        fetchAPIEN
        
        Args:
            key_name: EN
            
        Returns:
            APIEN，ifdoes not existENthenreturnNone
        """
        if key_name not in self.keys:
            return None
        
        key_info = self.keys[key_name]
        
        # checkEN
        if not key_info.get("is_active", True):
            logger.warning(f"APIEN '{key_name}' EN")
            return None
        
        # checkEN
        if key_info.get("expires_at"):
            expires_at = datetime.fromisoformat(key_info["expires_at"])
            if datetime.now() > expires_at:
                logger.warning(f"APIEN '{key_name}' EN")
                return None
        
        # updateuseEN
        key_info["last_used"] = datetime.now().isoformat()
        key_info["usage_count"] = key_info.get("usage_count", 0) + 1
        self._save_keys()
        
        return key_info["api_key"]
    
    def get_active_api_key(self, provider: str = "dashscope") -> Optional[str]:
        """
        fetchENAPIEN
        
        Args:
            provider: EN
            
        Returns:
            ENAPIEN，ifENthenreturnNone
        """
        active_keys = []
        
        for key_name, key_info in self.keys.items():
            if (key_info.get("provider") == provider and 
                key_info.get("is_active", True)):
                
                # checkEN
                if key_info.get("expires_at"):
                    expires_at = datetime.fromisoformat(key_info["expires_at"])
                    if datetime.now() > expires_at:
                        continue
                
                active_keys.append((key_name, key_info))
        
        if not active_keys:
            return None
        
        # ENreturnENuseEN
        active_keys.sort(key=lambda x: x[1].get("last_used", ""), reverse=True)
        return active_keys[0][1]["api_key"]
    
    def remove_api_key(self, key_name: str) -> bool:
        """
        deleteAPIEN
        
        Args:
            key_name: EN
            
        Returns:
            ENdeletesucceeded
        """
        if key_name not in self.keys:
            logger.warning(f"APIEN '{key_name}' does not exist")
            return False
        
        del self.keys[key_name]
        self.metadata["last_updated"] = datetime.now().isoformat()
        self.metadata["total_keys"] = len(self.keys)
        self._save_keys()
        
        logger.info(f"succeededdeleteAPIEN: {key_name}")
        return True
    
    def update_api_key(self, key_name: str, **updates) -> bool:
        """
        updateAPIEN
        
        Args:
            key_name: EN
            **updates: ENupdateEN
            
        Returns:
            ENupdatesucceeded
        """
        if key_name not in self.keys:
            logger.warning(f"APIEN '{key_name}' does not exist")
            return False
        
        # ENupdateEN
        allowed_fields = ["description", "expires_at", "is_active"]
        
        for field, value in updates.items():
            if field in allowed_fields:
                if field == "expires_at" and value is not None:
                    if isinstance(value, datetime):
                        value = value.isoformat()
                self.keys[key_name][field] = value
        
        self.metadata["last_updated"] = datetime.now().isoformat()
        self._save_keys()
        
        logger.info(f"succeededupdateAPIEN: {key_name}")
        return True
    
    def list_api_keys(self) -> List[Dict[str, Any]]:
        """
        ENallAPIEN（EN）
        
        Returns:
            APIEN
        """
        result = []
        
        for key_name, key_info in self.keys.items():
            # ENreturnENAPIEN
            safe_info = {
                "name": key_name,
                "provider": key_info.get("provider"),
                "description": key_info.get("description"),
                "created_at": key_info.get("created_at"),
                "expires_at": key_info.get("expires_at"),
                "last_used": key_info.get("last_used"),
                "usage_count": key_info.get("usage_count", 0),
                "is_active": key_info.get("is_active", True)
            }
            
            # checkEN
            if key_info.get("expires_at"):
                expires_at = datetime.fromisoformat(key_info["expires_at"])
                safe_info["is_expired"] = datetime.now() > expires_at
            else:
                safe_info["is_expired"] = False
            
            result.append(safe_info)
        
        return result
    
    def test_api_key(self, key_name: str) -> Dict[str, Any]:
        """
        ENAPIEN
        
        Args:
            key_name: EN
            
        Returns:
            ENresult
        """
        api_key = self.get_api_key(key_name)
        if not api_key:
            return {
                "success": False,
                "error": "ENdoes not existEN"
            }
        
        try:
            # ENcanENAPIEN
            # ENvalidate
            if self._validate_api_key_format(api_key, "dashscope"):
                return {
                    "success": True,
                    "message": "APIEN"
                }
            else:
                return {
                    "success": False,
                    "error": "APIEN"
                }
        except Exception as e:
            return {
                "success": False,
                "error": f"ENfailed: {str(e)}"
            }
    
    def _validate_api_key_format(self, api_key: str, provider: str) -> bool:
        """
        validateAPIEN
        
        Args:
            api_key: APIEN
            provider: EN
            
        Returns:
            EN
        """
        if not api_key or len(api_key.strip()) < 10:
            return False
        
        if provider == "dashscope":
            # DashScope APIENsk-EN
            return api_key.startswith("sk-") and len(api_key) >= 20
        
        # ENcanENvalidateEN
        return True
    
    def rotate_api_key(self, key_name: str, new_api_key: str) -> bool:
        """
        ENAPIEN
        
        Args:
            key_name: EN
            new_api_key: ENAPIEN
            
        Returns:
            ENsucceeded
        """
        if key_name not in self.keys:
            logger.warning(f"APIEN '{key_name}' does not exist")
            return False
        
        old_key_info = self.keys[key_name]
        
        # validateEN
        if not self._validate_api_key_format(new_api_key, old_key_info.get("provider", "dashscope")):
            raise ValidationError("ENAPIEN")
        
        # updateEN
        self.keys[key_name]["api_key"] = new_api_key
        self.keys[key_name]["rotated_at"] = datetime.now().isoformat()
        self.keys[key_name]["last_used"] = None
        self.keys[key_name]["usage_count"] = 0
        
        self.metadata["last_updated"] = datetime.now().isoformat()
        self._save_keys()
        
        logger.info(f"succeededENAPIEN: {key_name}")
        return True
    
    def get_usage_statistics(self) -> Dict[str, Any]:
        """
        fetchuseEN
        
        Returns:
            useEN
        """
        total_keys = len(self.keys)
        active_keys = sum(1 for k in self.keys.values() if k.get("is_active", True))
        expired_keys = 0
        total_usage = 0
        
        for key_info in self.keys.values():
            if key_info.get("expires_at"):
                expires_at = datetime.fromisoformat(key_info["expires_at"])
                if datetime.now() > expires_at:
                    expired_keys += 1
            
            total_usage += key_info.get("usage_count", 0)
        
        return {
            "total_keys": total_keys,
            "active_keys": active_keys,
            "expired_keys": expired_keys,
            "total_usage": total_usage,
            "last_updated": self.metadata.get("last_updated")
        }
    
    def cleanup_expired_keys(self) -> int:
        """
        ENAPIEN
        
        Returns:
            EN
        """
        cleaned_count = 0
        current_time = datetime.now()
        
        keys_to_remove = []
        
        for key_name, key_info in self.keys.items():
            if key_info.get("expires_at"):
                expires_at = datetime.fromisoformat(key_info["expires_at"])
                if current_time > expires_at:
                    keys_to_remove.append(key_name)
        
        for key_name in keys_to_remove:
            self.remove_api_key(key_name)
            cleaned_count += 1
        
        if cleaned_count > 0:
            logger.info(f"EN {cleaned_count} ENAPIEN")
        
        return cleaned_count

# ENAPIEN
api_key_manager = APIKeyManager()

def get_api_key(key_name: Optional[str] = None, provider: str = "dashscope") -> Optional[str]:
    """
    fetchAPIEN
    
    Args:
        key_name: EN，ifENNonethenfetchEN
        provider: EN
        
    Returns:
        APIEN
    """
    if key_name:
        return api_key_manager.get_api_key(key_name)
    else:
        return api_key_manager.get_active_api_key(provider)

def set_api_key(api_key: str, key_name: str = "default", provider: str = "dashscope") -> bool:
    """
    settingsAPIEN
    
    Args:
        api_key: APIEN
        key_name: EN
        provider: EN
        
    Returns:
        ENsettingssucceeded
    """
    return api_key_manager.add_api_key(key_name, api_key, provider) 