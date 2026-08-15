from fastapi import HTTPException
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models import Author, Book
from app.schemas.author import AuthorCreate, AuthorUpdate


def list_authors(db: Session) -> list[Author]:
    stmt = select(Author).order_by(Author.id)
    return list(db.scalars(stmt).all())


def get_author(db: Session, author_id: int) -> Author:
    author = db.get(Author, author_id)
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    return author


def create_author(db: Session, payload: AuthorCreate) -> Author:
    author = Author(**payload.model_dump())
    db.add(author)
    db.commit()
    db.refresh(author)
    return author


def update_author(db: Session, author_id: int, payload: AuthorUpdate) -> Author:
    author = get_author(db, author_id)

    for field, value in payload.model_dump(exclude_unset=True).items():
        if value is not None:
            setattr(author, field, value)

    db.commit()
    db.refresh(author)
    return author


def delete_author(db: Session, author_id: int) -> None:
    author = get_author(db, author_id)

    stmt = select(func.count()).select_from(Book).where(Book.author_id == author_id)
    book_count = db.scalar(stmt) or 0

    if book_count > 0:
        raise HTTPException(
            status_code=409,
            detail="Cannot delete author while books exist"
        )

    db.delete(author)
    db.commit()