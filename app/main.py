from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.admin import setup_admin
from app.api.routers import auth, books, users 
from app.core.config import get_settings
from app.db.database import Base
from app.db.session import engine
from app.models import Book, User  

settings = get_settings()
app = FastAPI(title=settings.app_title)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173", 
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)
setup_admin(app, engine)

app.include_router(books.router, prefix="/api/v1")
app.include_router(users.router, prefix="/api/v1") 
app.include_router(auth.router, prefix="/api/v1") 


@app.get("/")
def root() -> dict[str, str]:
    return {"message": "Hello World"}