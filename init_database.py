#!/usr/bin/env python3
"""
ENScript
"""

import sys
from pathlib import Path

# ENProjectEN
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))
sys.path.insert(0, str(current_dir / "backend"))

# EN
import os
os.chdir(current_dir)

def init_database():
    """EN"""
    print("🚀 EN...")
    
    try:
        # ENAllEN
        from backend.models import Base, BilibiliAccount, UploadRecord
        from backend.core.database import init_database, create_tables
        
        print("✅ AllENSuccess")
        
        # EN
        if init_database():
            print("✅ ENSuccess")
        else:
            print("❌ ENFailed")
            return False
        
        # EN
        create_tables()
        print("✅ ENSuccess")
        
        return True
        
    except Exception as e:
        print(f"❌ ENFailed: {e}")
        return False

if __name__ == "__main__":
    success = init_database()
    if success:
        print("\n🎉 ENCompleted！")
        print("ENStartSystemEN：")
        print("1. ./start_autoclip_with_upload.sh")
        print("2. ENManualStartENService")
    else:
        print("\n❌ ENFailed，PleaseCheckErrorEN")
        sys.exit(1)

