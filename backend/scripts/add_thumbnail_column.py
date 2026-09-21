#!/usr/bin/env python3
"""
ENthumbnailENprojectsEN
"""

import sys
from pathlib import Path

# ENbackenddirectoryENPythonpath
backend_dir = Path(__file__).parent.parent
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

# ENprojectENdirectoryENPythonpath
project_root = Path(__file__).parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from backend.core.database import engine, SessionLocal
from sqlalchemy import text

def add_thumbnail_column():
    """ENthumbnailENprojectsEN"""
    try:
        # checkENalready exists
        with engine.connect() as conn:
            # ENSQLite，checkEN
            result = conn.execute(text("PRAGMA table_info(projects)"))
            columns = [row[1] for row in result.fetchall()]
            
            if 'thumbnail' in columns:
                print("✅ thumbnailENalready exists，EN")
                return True
            
            # ENthumbnailEN
            conn.execute(text("ALTER TABLE projects ADD COLUMN thumbnail TEXT"))
            conn.commit()
            print("✅ succeededENthumbnailENprojectsEN")
            return True
            
    except Exception as e:
        print(f"❌ ENthumbnailENfailed: {e}")
        return False

def main():
    """EN"""
    print("🚀 startENthumbnailEN...")
    
    if add_thumbnail_column():
        print("🎉 thumbnailEN！")
    else:
        print("❌ thumbnailENfailed")
        sys.exit(1)

if __name__ == "__main__":
    main()
