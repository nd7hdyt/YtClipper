"""
databaseconfig
Packageincludedatabaseconnect、translatedAnddependenciestranslated
"""

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool
from typing import Generator
from backend.models.base import Base

# databaseconfig
DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "sqlite:///autoclip.db"
)

# iftranslatedsettingstranslated，useconfigtranslatedfetchdatabaseURL
if DATABASE_URL == "sqlite:///autoclip.db":
    try:
        from .config import get_database_url
        DATABASE_URL = get_database_url()
    except ImportError:
        # iftranslatedimportfailed，translateddefaulttranslated
        pass

# createdatabasetranslated
if "sqlite" in DATABASE_URL:
    # SQLiteconfig。
    # StaticPool = translated processtranslatedonetranslatedconnect，translated :memory:。filetranslatedusetranslated，translated API translated、
    # importtasktranslated、translated's Session translatedintranslatedonetranslatedconnecttranslated BEGIN / COMMIT / ROLLBACK：
    # one translated close() translated's ROLLBACK translated translatedone translated INSERT translated COMMIT 's Task translated
    # （translated ObjectDeletedError、tasktranslated、progresstranslated）。filetranslatedusedefaultconnecttranslated，per  Session onetranslatedconnect，
    # translated WAL translated。
    _is_memory_db = DATABASE_URL.rstrip("/") in ("sqlite://", "sqlite:///:memory:") or ":memory:" in DATABASE_URL
    _sqlite_kwargs = {"poolclass": StaticPool} if _is_memory_db else {}
    engine = create_engine(
        DATABASE_URL,
        connect_args={
            "check_same_thread": False,
            "timeout": 30
        },
        pool_pre_ping=True,
        echo=False,  # settingstranslatedTruecantranslatedSQLtranslated
        **_sqlite_kwargs,
    )
    if not _is_memory_db:
        from sqlalchemy import event

        @event.listens_for(engine, "connect")
        def _sqlite_pragmas(dbapi_connection, _record):
            cursor = dbapi_connection.cursor()
            try:
                cursor.execute("PRAGMA journal_mode=WAL")
                cursor.execute("PRAGMA busy_timeout=30000")
            finally:
                cursor.close()
else:
    # PostgreSQLconfig
    engine = create_engine(
        DATABASE_URL,
        pool_pre_ping=True,
        pool_recycle=300,
        echo=False
    )

# createtranslated
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

def get_db() -> Generator[Session, None, None]:
    """
    databasetranslateddependenciestranslated
    usetranslatedFastAPI'sdependenciestranslatedSystem
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_tables():
    """createtranslateddatabasetranslated"""
    Base.metadata.create_all(bind=engine)

def drop_tables():
    """deletetranslateddatabasetranslated"""
    Base.metadata.drop_all(bind=engine)

def reset_database():
    """translateddatabase"""
    drop_tables()
    create_tables()

from sqlalchemy import text

def test_connection() -> bool:
    """testdatabaseconnect"""
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1")).fetchone()
        return True
    except Exception as e:
        print(f"databaseconnecttestfailed: {e}")
        return False

# databasetranslated
def init_database():
    """translateddatabase"""
    print("translatedintranslateddatabase...")
    
    # testconnect
    if not test_connection():
        print("❌ databaseconnectfailed")
        return False
    
    # createtranslated
    try:
        create_tables()
        print("✅ databasetranslatedcreatesucceeded")
        return True
    except Exception as e:
        print(f"❌ databasetranslatedcreatefailed: {e}")
        return False

if __name__ == "__main__":
    # translatedfiletranslateddatabase
    init_database()