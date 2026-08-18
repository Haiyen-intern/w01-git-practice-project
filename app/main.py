from fastapi import FastAPI

from app.admin import setup_admin
from app.core.config import get_settings
from app.db.database import Base
from app.db.session import engine

settings = get_settings()
app = FastAPI(title=settings.app_title)

Base.metadata.create_all(bind=engine)
setup_admin(app, engine)


@app.get("/")
def root() -> dict[str, str]:
    return {"message": "Hello World"}
