from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.book import BookCreate, BookRead, BookUpdate
from app.services import book_service

router = APIRouter(tags=["books"])


@router.get("/books", response_model=list[BookRead])
def list_books(db: Session = Depends(get_db)) -> list[BookRead]:
    return book_service.list_books(db)


@router.get("/books/{book_id}", response_model=BookRead)
def get_book(book_id: int, db: Session = Depends(get_db)) -> BookRead:
    return book_service.get_book(db, book_id)


@router.post("/books", response_model=BookRead, status_code=201)
def create_book(
    payload: BookCreate,
    db: Session = Depends(get_db),
) -> BookRead:
    return book_service.create_book(db, payload)


@router.put("/books/{book_id}", response_model=BookRead)
def update_book(
    book_id: int,
    payload: BookUpdate,
    db: Session = Depends(get_db),
) -> BookRead:
    return book_service.update_book(db, book_id, payload)


@router.delete("/books/{book_id}", status_code=204)
def delete_book(book_id: int, db: Session = Depends(get_db)) -> None:
    book_service.delete_book(db, book_id)