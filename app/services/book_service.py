from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Book
from app.schemas.book import BookCreate, BookUpdate


def list_books(db: Session) -> list[Book]:
    stmt = select(Book).order_by(Book.id)
    return list(db.scalars(stmt))


def get_book(db: Session, book_id: int) -> Book:
    book = db.get(Book, book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


def create_book(db: Session, payload: BookCreate) -> Book:
    book = Book(**payload.model_dump())
    db.add(book)
    db.commit()
    db.refresh(book)
    return book


def update_book(db: Session, book_id: int, payload: BookUpdate) -> Book:
    book = get_book(db, book_id)
    for key, value in payload.model_dump().items():
        setattr(book, key, value)
    db.commit()
    db.refresh(book)
    return book


def delete_book(db: Session, book_id: int) -> None:
    book = get_book(db, book_id)
    db.delete(book)
    db.commit()