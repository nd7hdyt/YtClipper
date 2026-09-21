#!/usr/bin/env python3
"""
addthumbnailtranslatedprojectstranslated'stranslated
"""

import sys
from pathlib import Path

# addbackenddirectorytranslatedPythonpath
backend_dir = Path(__file__).parent.parent
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

# addprojecttranslateddirectorytranslatedPythonpath
project_root = Path(__file__).parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from backend.core.database import engine, SessionLocal
from sqlalchemy import text

def add_thumbnail_column():
    """addthumbnailtranslatedprojectstranslated"""
    try:
        # checktranslatedIstranslatedin
        with engine.connect() as conn:
            # translatedSQLite，checktranslated
            result = conn.execute(text("PRAGMA table_info(projects)"))
            columns = [row[1] for row in result.fetchall()]
            
            if 'thumbnail' in columns:
                print("✅ thumbnailtranslatedin，translatedadd")
                return True
            
            # addthumbnailtranslated
            conn.execute(text("ALTER TABLE projects ADD COLUMN thumbnail TEXT"))
            conn.commit()
            print("✅ succeededaddthumbnailtranslatedprojectstranslated")
            return True
            
    except Exception as e:
        print(f"❌ addthumbnailtranslatedfailed: {e}")
        return False

def main():
    """translated"""
    print("🚀 translatedaddthumbnailtranslated...")
    
    if add_thumbnail_column():
        print("🎉 thumbnailtranslatedaddtranslated！")
    else:
        print("❌ thumbnailtranslatedaddfailed")
        sys.exit(1)

if __name__ == "__main__":
    main()
