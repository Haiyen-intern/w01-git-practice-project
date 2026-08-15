from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from app.models import Book, Category
from app.schemas.book import BookCreate, BookRead, BookUpdate
from app.services.author_service import get_author


def _ensure_category_exists(db: Session, category_id: int | None) -> None:
    if category_id is not None:
        category = db.get(Category, category_id)
        if not category:
            raise HTTPException(status_code=404, detail="Category not found")


def to_book_read(book: Book) -> BookRead:
    return BookRead(
        id=book.id,
        title=book.title,
        year=book.year,
        summary=book.summary,
        author_id=book.author_id,
        author_name=book.author.name if book.author else None,
        category_id=book.category_id,
        category_name=book.category.name if book.category else None,
    )


def list_books(db: Session) -> list[BookRead]:
    stmt = (
        select(Book)
        .options(joinedload(Book.author), joinedload(Book.category))
        .order_by(Book.id)
    )
    books = db.scalars(stmt).all()
    return [to_book_read(b) for b in books]


def get_book(db: Session, book_id: int) -> BookRead:
    stmt = (
        select(Book)
        .options(joinedload(Book.author), joinedload(Book.category))
        .where(Book.id == book_id)
    )
    book = db.scalar(stmt)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return to_book_read(book)


def create_book(db: Session, payload: BookCreate) -> BookRead:
    if payload.author_id is not None:
        get_author(db, payload.author_id)
    _ensure_category_exists(db, payload.category_id)

    book = Book(**payload.model_dump())
    db.add(book)
    db.commit()
    db.refresh(book)
    return get_book(db, book.id)


def update_book(db: Session, book_id: int, payload: BookUpdate) -> BookRead:
    stmt = (
        select(Book)
        .options(joinedload(Book.author), joinedload(Book.category))
        .where(Book.id == book_id)
    )
    book = db.scalar(stmt)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    if payload.author_id is not None:
        get_author(db, payload.author_id)
    _ensure_category_exists(db, payload.category_id)

    for key, value in payload.model_dump().items():
        setattr(book, key, value)

    db.commit()
    db.refresh(book)
    return get_book(db, book.id)


def delete_book(db: Session, book_id: int) -> None:
    book = db.get(Book, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    db.delete(book)
    db.commit()


def search_books(
    db: Session,
    *,
    author_id: int | None = None,
    category_id: int | None = None,
    year_from: int | None = None,
    year_to: int | None = None,
    q: str | None = None,
) -> list[BookRead]:
    stmt = select(Book).options(
        joinedload(Book.author),
        joinedload(Book.category),  
    )

    if author_id is not None:
        stmt = stmt.where(Book.author_id == author_id)

    if category_id is not None:
        stmt = stmt.where(Book.category_id == category_id)

    if year_from is not None:
        stmt = stmt.where(Book.year >= year_from)  

    if year_to is not None:
        stmt = stmt.where(Book.year <= year_to) 

    if q:
        stmt = stmt.where(Book.title.ilike(f"%{q}%"))

    stmt = stmt.order_by(Book.id)
    books = db.scalars(stmt).all()
    return [to_book_read(b) for b in books]