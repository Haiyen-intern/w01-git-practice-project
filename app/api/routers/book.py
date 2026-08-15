from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.book import BookCreate, BookRead, BookUpdate
from app.services import book_service

router = APIRouter(prefix="/books", tags=["books"])


@router.get("/search", response_model=list[BookRead])
def search_books(
    db: Session = Depends(get_db),
    author_id: int | None = Query(default=None),
    category_id: int | None = Query(default=None),
    year_from: int | None = Query(default=None),
    year_to: int | None = Query(default=None),
    q: str | None = Query(default=None),
) -> list[BookRead]:
    return book_service.search_books(
        db,
        author_id=author_id,
        category_id=category_id,
        year_from=year_from,
        year_to=year_to,
        q=q,
    )


@router.get("/", response_model=list[BookRead])
def list_books(db: Session = Depends(get_db)) -> list[BookRead]:
    return book_service.list_books(db)


@router.get("/{book_id}", response_model=BookRead)
def get_book(book_id: int, db: Session = Depends(get_db)) -> BookRead:
    return book_service.get_book(db, book_id)


@router.post("/", response_model=BookRead, status_code=201)
def create_book(
    payload: BookCreate,
    db: Session = Depends(get_db),
) -> BookRead:
    return book_service.create_book(db, payload)


@router.put("/{book_id}", response_model=BookRead)
def update_book(
    book_id: int,
    payload: BookUpdate,
    db: Session = Depends(get_db),
) -> BookRead:
    return book_service.update_book(db, book_id, payload)


@router.delete("/{book_id}", status_code=204)
def delete_book(book_id: int, db: Session = Depends(get_db)) -> None:
    book_service.delete_book(db, book_id)