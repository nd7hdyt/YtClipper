"""
EN
ENcookies
"""

import os
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import logging

logger = logging.getLogger(__name__)

# fetchEN
def get_encryption_key():
    """fetchEN"""
    # ENfetchEN，ifENthengenerateEN
    key = os.getenv('ENCRYPTION_KEY')
    if not key:
        # generateEN
        key = Fernet.generate_key()
        logger.warning("ENCRYPTION_KEYENsettings，useEN。pleasesettingsEN。")
    
    if isinstance(key, str):
        key = key.encode()
    
    return key

def encrypt_data(data: str) -> str:
    """EN"""
    try:
        key = get_encryption_key()
        f = Fernet(key)
        encrypted_data = f.encrypt(data.encode())
        return base64.b64encode(encrypted_data).decode()
    except Exception as e:
        logger.error(f"ENfailed: {str(e)}")
        raise

def decrypt_data(encrypted_data: str) -> str:
    """EN"""
    try:
        key = get_encryption_key()
        f = Fernet(key)
        decoded_data = base64.b64decode(encrypted_data.encode())
        decrypted_data = f.decrypt(decoded_data)
        return decrypted_data.decode()
    except Exception as e:
        logger.error(f"ENfailed: {str(e)}")
        raise

