from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session 
from app.db.session import get_db
from app.schemas.author import AuthorCreate, AuthorRead, AuthorUpdate
from app.services import author_service

router = APIRouter(prefix="/authors", tags=["authors"])

@router.get("/", response_model=list[AuthorRead])
def list_authors(db: Session = Depends(get_db)) -> list[AuthorRead]:
    return author_service.list_authors(db)

@router.get("/{author_id}", response_model=AuthorRead)
def get_author(author_id: int, db: Session = Depends(get_db)) -> AuthorRead:
    return author_service.get_author(db, author_id)

@router.post("/", response_model=AuthorRead, status_code=201)
def create_author(
    payload: AuthorCreate,
    db: Session = Depends(get_db),
) -> AuthorRead:
    return author_service.create_author(db, payload)

@router.put("/{author_id}", response_model=AuthorRead)
def update_author(
    author_id: int,
    payload: AuthorUpdate,
    db: Session = Depends(get_db),
) -> AuthorRead:
    return author_service.update_author(db, author_id, payload)

@router.delete("/{author_id}", status_code=204)
def delete_author(author_id: int, db: Session = Depends(get_db)) -> None:
    author_service.delete_author(db, author_id)
