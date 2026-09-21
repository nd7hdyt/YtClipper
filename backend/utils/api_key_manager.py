"""
APIkeytranslatedSystem - Providestranslated'skeytranslated、verifyAndtranslatedfeature
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
    """APIkeytranslated"""
    
    def __init__(self, storage_path: Optional[Path] = None, master_password: Optional[str] = None):
        """
        translatedAPIkeytranslated
        
        Args:
            storage_path: keytranslatedpath
            master_password: translated，usetranslated
        """
        self.storage_path = storage_path or Path.home() / ".auto_clips" / "api_keys"
        self.master_password = master_password or self._get_master_password()
        self.fernet = self._create_fernet()
        self.keys_file = self.storage_path / "keys.enc"
        self.metadata_file = self.storage_path / "metadata.json"
        
        # ensuretranslateddirectorytranslatedin
        self.storage_path.mkdir(parents=True, exist_ok=True)
        
        # translatedkey
        self._load_keys()
    
    def _get_master_password(self) -> str:
        """fetchtranslated"""
        # translatedfromtranslatedfetch
        master_password = os.getenv("AUTO_CLIPS_MASTER_PASSWORD")
        if master_password:
            return master_password
        
        # iftranslatedsettings，usedefaulttranslated（Onlyusetranslated）
        if os.getenv("AUTO_CLIPS_DEV_MODE"):
            return "dev_master_password"
        
        # translatedsettingstranslated
        raise ConfigurationError(
            "translatedsettingstranslated。translatedsettings AUTO_CLIPS_MASTER_PASSWORD translated。"
        )
    
    def _create_fernet(self) -> Fernet:
        """createFernettranslated"""
        # usetranslatedkey
        salt = b'auto_clips_salt'  # intranslatedusetranslatedusetranslatedsalt
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(self.master_password.encode()))
        return Fernet(key)
    
    def _load_keys(self):
        """translated'skey"""
        self.keys: Dict[str, Dict[str, Any]] = {}
        
        if self.keys_file.exists():
            try:
                with open(self.keys_file, 'rb') as f:
                    encrypted_data = f.read()
                    decrypted_data = self.fernet.decrypt(encrypted_data)
                    self.keys = json.loads(decrypted_data.decode())
                logger.info(f"succeededtranslated {len(self.keys)}  APIkey")
            except Exception as e:
                logger.warning(f"translatedAPIkeyfailed: {e}")
                self.keys = {}
        
        # translated
        self.metadata: Dict[str, Any] = {}
        if self.metadata_file.exists():
            try:
                with open(self.metadata_file, 'r', encoding='utf-8') as f:
                    self.metadata = json.load(f)
            except Exception as e:
                logger.warning(f"translatedAPIkeytranslatedfailed: {e}")
                self.metadata = {}
    
    def _save_keys(self):
        """translatedkeytranslatedfile"""
        try:
            # translatedkey
            data = json.dumps(self.keys, ensure_ascii=False)
            encrypted_data = self.fernet.encrypt(data.encode())
            
            with open(self.keys_file, 'wb') as f:
                f.write(encrypted_data)
            
            # translated（translated）
            with open(self.metadata_file, 'w', encoding='utf-8') as f:
                json.dump(self.metadata, f, ensure_ascii=False, indent=2)
            
            logger.debug("APIkeytranslated")
        except Exception as e:
            logger.error(f"translatedAPIkeyfailed: {e}")
            raise ConfigurationError(f"translatedAPIkeyfailed: {e}")
    
    def add_api_key(self, key_name: str, api_key: str, provider: str = "dashscope", 
                   description: str = "", expires_at: Optional[datetime] = None) -> bool:
        """
        addAPIkey
        
        Args:
            key_name: keytranslated
            api_key: APIkeytranslated
            provider: Providesprovider（ifdashscope）
            description: translatedinfo
            expires_at: translated
            
        Returns:
            Istranslatedaddsucceeded
        """
        try:
            # verifykeyformat
            if not self._validate_api_key_format(api_key, provider):
                raise ValidationError(f"translated's{provider} APIkeyformat")
            
            # checkkeyIstranslatedin
            if key_name in self.keys:
                logger.warning(f"keytranslated '{key_name}' translatedin，translated")
            
            # translatedkeyinfo
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
            
            # updatetranslated
            self.metadata["last_updated"] = datetime.now().isoformat()
            self.metadata["total_keys"] = len(self.keys)
            
            # translatedfile
            self._save_keys()
            
            logger.info(f"succeededaddAPIkey: {key_name}")
            return True
            
        except Exception as e:
            logger.error(f"addAPIkeyfailed: {e}")
            raise
    
    def get_api_key(self, key_name: str) -> Optional[str]:
        """
        fetchAPIkey
        
        Args:
            key_name: keytranslated
            
        Returns:
            APIkeytranslated，iftranslatednot foundortranslatedreturnNone
        """
        if key_name not in self.keys:
            return None
        
        key_info = self.keys[key_name]
        
        # checkIstranslated
        if not key_info.get("is_active", True):
            logger.warning(f"APIkey '{key_name}' translateduse")
            return None
        
        # checkIstranslated
        if key_info.get("expires_at"):
            expires_at = datetime.fromisoformat(key_info["expires_at"])
            if datetime.now() > expires_at:
                logger.warning(f"APIkey '{key_name}' translated")
                return None
        
        # updateusetranslated
        key_info["last_used"] = datetime.now().isoformat()
        key_info["usage_count"] = key_info.get("usage_count", 0) + 1
        self._save_keys()
        
        return key_info["api_key"]
    
    def get_active_api_key(self, provider: str = "dashscope") -> Optional[str]:
        """
        fetchtranslated'sAPIkey
        
        Args:
            provider: Providesprovider
            
        Returns:
            translated'sAPIkey，iftranslatedreturnNone
        """
        active_keys = []
        
        for key_name, key_info in self.keys.items():
            if (key_info.get("provider") == provider and 
                key_info.get("is_active", True)):
                
                # checkIstranslated
                if key_info.get("expires_at"):
                    expires_at = datetime.fromisoformat(key_info["expires_at"])
                    if datetime.now() > expires_at:
                        continue
                
                active_keys.append((key_name, key_info))
        
        if not active_keys:
            return None
        
        # translatedreturntranslateduse'skey
        active_keys.sort(key=lambda x: x[1].get("last_used", ""), reverse=True)
        return active_keys[0][1]["api_key"]
    
    def remove_api_key(self, key_name: str) -> bool:
        """
        deleteAPIkey
        
        Args:
            key_name: keytranslated
            
        Returns:
            Istranslateddeletesucceeded
        """
        if key_name not in self.keys:
            logger.warning(f"APIkey '{key_name}' not found")
            return False
        
        del self.keys[key_name]
        self.metadata["last_updated"] = datetime.now().isoformat()
        self.metadata["total_keys"] = len(self.keys)
        self._save_keys()
        
        logger.info(f"succeededdeleteAPIkey: {key_name}")
        return True
    
    def update_api_key(self, key_name: str, **updates) -> bool:
        """
        updateAPIkeyinfo
        
        Args:
            key_name: keytranslated
            **updates: translatedupdate'stranslated
            
        Returns:
            Istranslatedupdatesucceeded
        """
        if key_name not in self.keys:
            logger.warning(f"APIkey '{key_name}' not found")
            return False
        
        # translatedupdate'stranslated
        allowed_fields = ["description", "expires_at", "is_active"]
        
        for field, value in updates.items():
            if field in allowed_fields:
                if field == "expires_at" and value is not None:
                    if isinstance(value, datetime):
                        value = value.isoformat()
                self.keys[key_name][field] = value
        
        self.metadata["last_updated"] = datetime.now().isoformat()
        self._save_keys()
        
        logger.info(f"succeededupdateAPIkey: {key_name}")
        return True
    
    def list_api_keys(self) -> List[Dict[str, Any]]:
        """
        translatedAPIkey（translatedPackageincludetranslatedkeytranslated）
        
        Returns:
            APIkeyinfolist
        """
        result = []
        
        for key_name, key_info in self.keys.items():
            # translatedreturntranslated'sAPIkeytranslated
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
            
            # checkIstranslated
            if key_info.get("expires_at"):
                expires_at = datetime.fromisoformat(key_info["expires_at"])
                safe_info["is_expired"] = datetime.now() > expires_at
            else:
                safe_info["is_expired"] = False
            
            result.append(safe_info)
        
        return result
    
    def test_api_key(self, key_name: str) -> Dict[str, Any]:
        """
        testAPIkey
        
        Args:
            key_name: keytranslated
            
        Returns:
            testtranslated
        """
        api_key = self.get_api_key(key_name)
        if not api_key:
            return {
                "success": False,
                "error": "keynot foundortranslated"
            }
        
        try:
            # thistranslatedcantranslatedaddtranslated'sAPItesttranslated
            # translatedIstranslated'sformatverify
            if self._validate_api_key_format(api_key, "dashscope"):
                return {
                    "success": True,
                    "message": "APIkeyformattranslated"
                }
            else:
                return {
                    "success": False,
                    "error": "APIkeyformattranslated"
                }
        except Exception as e:
            return {
                "success": False,
                "error": f"testfailed: {str(e)}"
            }
    
    def _validate_api_key_format(self, api_key: str, provider: str) -> bool:
        """
        verifyAPIkeyformat
        
        Args:
            api_key: APIkey
            provider: Providesprovider
            
        Returns:
            formatIstranslated
        """
        if not api_key or len(api_key.strip()) < 10:
            return False
        
        if provider == "dashscope":
            # DashScope APIkeytranslatedIssk-translated'stranslated
            return api_key.startswith("sk-") and len(api_key) >= 20
        
        # translatedProvidesprovidercantranslatedaddtranslated'sverifytranslated
        return True
    
    def rotate_api_key(self, key_name: str, new_api_key: str) -> bool:
        """
        translatedAPIkey
        
        Args:
            key_name: keytranslated
            new_api_key: translated'sAPIkey
            
        Returns:
            Istranslatedsucceeded
        """
        if key_name not in self.keys:
            logger.warning(f"APIkey '{key_name}' not found")
            return False
        
        old_key_info = self.keys[key_name]
        
        # verifytranslatedkeyformat
        if not self._validate_api_key_format(new_api_key, old_key_info.get("provider", "dashscope")):
            raise ValidationError("translatedAPIkeyformattranslated")
        
        # updatekey
        self.keys[key_name]["api_key"] = new_api_key
        self.keys[key_name]["rotated_at"] = datetime.now().isoformat()
        self.keys[key_name]["last_used"] = None
        self.keys[key_name]["usage_count"] = 0
        
        self.metadata["last_updated"] = datetime.now().isoformat()
        self._save_keys()
        
        logger.info(f"succeededtranslatedAPIkey: {key_name}")
        return True
    
    def get_usage_statistics(self) -> Dict[str, Any]:
        """
        fetchusetranslated
        
        Returns:
            usetranslatedinfo
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
        cleantranslated'sAPIkey
        
        Returns:
            clean'skeytranslated
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
            logger.info(f"cleantranslated {cleaned_count}  translated'sAPIkey")
        
        return cleaned_count

# translatedAPIkeytranslated
api_key_manager = APIKeyManager()

def get_api_key(key_name: Optional[str] = None, provider: str = "dashscope") -> Optional[str]:
    """
    fetchAPIkey'stranslated
    
    Args:
        key_name: keytranslated，iftranslatedNonetranslatedfetchtranslatedkey
        provider: Providesprovider
        
    Returns:
        APIkey
    """
    if key_name:
        return api_key_manager.get_api_key(key_name)
    else:
        return api_key_manager.get_active_api_key(provider)

def set_api_key(api_key: str, key_name: str = "default", provider: str = "dashscope") -> bool:
    """
    settingsAPIkey'stranslated
    
    Args:
        api_key: APIkey
        key_name: keytranslated
        provider: Providesprovider
        
    Returns:
        Istranslatedsettingssucceeded
    """
    return api_key_manager.add_api_key(key_name, api_key, provider) 