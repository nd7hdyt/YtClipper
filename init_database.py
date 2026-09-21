#!/usr/bin/env python3
"""
databasetranslated
"""

import sys
from pathlib import Path

# addprojecttranslateddirectorytranslatedpath
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))
sys.path.insert(0, str(current_dir / "backend"))

# settingstranslateddirectory
import os
os.chdir(current_dir)

def init_database():
    """translateddatabase"""
    print("🚀 translateddatabase...")
    
    try:
        # importtranslatedmodelensuretranslatedcreate
        from backend.models import Base, BilibiliAccount, UploadRecord
        from backend.core.database import init_database, create_tables
        
        print("✅ translatedmodelimportsucceeded")
        
        # translateddatabase
        if init_database():
            print("✅ databasetranslatedsucceeded")
        else:
            print("❌ databasetranslatedfailed")
            return False
        
        # createtranslated
        create_tables()
        print("✅ databasetranslatedcreatesucceeded")
        
        return True
        
    except Exception as e:
        print(f"❌ databasetranslatedfailed: {e}")
        return False

if __name__ == "__main__":
    success = init_database()
    if success:
        print("\n🎉 databasetranslated！")
        print("translatedincantranslatedstartSystemtranslated：")
        print("1. ./start_autoclip_with_upload.sh")
        print("2. ortranslatedstarttranslated service")
    else:
        print("\n❌ databasetranslatedfailed，translatedcheckerrorinfo")
        sys.exit(1)

