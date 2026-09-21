"""
databaseconfig
ENdatabaseconnect、EN
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

# ifENsettingsEN，useconfigENfetchdatabaseURL
if DATABASE_URL == "sqlite:///autoclip.db":
    try:
        from .config import get_database_url
        DATABASE_URL = get_database_url()
    except ImportError:
        # ifENfailed，EN
        pass

# createdatabaseEN
if "sqlite" in DATABASE_URL:
    # SQLiteconfig。
    # StaticPool = ENconnect，EN :memory:。fileEN，EN API requestEN、
    # ENtaskEN、EN Session ENconnectEN BEGIN / COMMIT / ROLLBACK：
    # EN close() EN ROLLBACK EN INSERT EN COMMIT EN Task EN
    # （EN ObjectDeletedError、taskEN、progressEN）。fileENconnectEN，each Session ENconnect，
    # EN WAL EN。
    _is_memory_db = DATABASE_URL.rstrip("/") in ("sqlite://", "sqlite:///:memory:") or ":memory:" in DATABASE_URL
    _sqlite_kwargs = {"poolclass": StaticPool} if _is_memory_db else {}
    engine = create_engine(
        DATABASE_URL,
        connect_args={
            "check_same_thread": False,
            "timeout": 30
        },
        pool_pre_ping=True,
        echo=False,  # settingsENTruecanENSQLEN
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

# createEN
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

def get_db() -> Generator[Session, None, None]:
    """
    databaseEN
    ENFastAPIENsystem
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_tables():
    """createalldatabaseEN"""
    Base.metadata.create_all(bind=engine)

def drop_tables():
    """deletealldatabaseEN"""
    Base.metadata.drop_all(bind=engine)

def reset_database():
    """ENdatabase"""
    drop_tables()
    create_tables()

from sqlalchemy import text

def test_connection() -> bool:
    """ENdatabaseconnect"""
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1")).fetchone()
        return True
    except Exception as e:
        print(f"databaseconnectENfailed: {e}")
        return False

# databaseinitialize
def init_database():
    """initializedatabase"""
    print("currentlyinitializedatabase...")
    
    # ENconnect
    if not test_connection():
        print("❌ databaseconnectfailed")
        return False
    
    # createEN
    try:
        create_tables()
        print("✅ databaseENcreatesucceeded")
        return True
    except Exception as e:
        print(f"❌ databaseENcreatefailed: {e}")
        return False

if __name__ == "__main__":
    # ENrunENfileENinitializedatabase
    init_database()