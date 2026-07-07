import os
from collections.abc import Generator

from sqlalchemy import create_engine, inspect, text
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker


DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./slp3_notes.db")

connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
engine = create_engine(DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


class Base(DeclarativeBase):
    pass


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db() -> None:
    from app.models import chapter, note, source  # noqa: F401

    Base.metadata.create_all(bind=engine)
    if DATABASE_URL.startswith("sqlite"):
        _ensure_sqlite_columns()


def _ensure_sqlite_columns() -> None:
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    with engine.begin() as conn:
        if "chapters" in tables:
            chapter_columns = {column["name"] for column in inspector.get_columns("chapters")}
            if "source_id" not in chapter_columns:
                conn.execute(text("ALTER TABLE chapters ADD COLUMN source_id INTEGER DEFAULT 1"))
        if "notes" in tables:
            note_columns = {column["name"] for column in inspector.get_columns("notes")}
            if "source_id" not in note_columns:
                conn.execute(text("ALTER TABLE notes ADD COLUMN source_id INTEGER DEFAULT 1"))
