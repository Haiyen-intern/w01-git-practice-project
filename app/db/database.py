from pathlib import Path

from sqlalchemy.orm import DeclarativeBase

from app.core.config import get_settings

DATA_DIR = Path(__file__).resolve().parent.parent.parent / "data"
DATA_DIR.mkdir(exist_ok=True)

settings = get_settings()
DATABASE_URL = settings.database_url or f"sqlite:///{DATA_DIR / 'books.db'}"


class Base(DeclarativeBase):
    pass
