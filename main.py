from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database import Base, engine, get_db
from app.models import Book

app = FastAPI(title="Books API")
Base.metadata.create_all(bind=engine)


class BookCreate(BaseModel):
    title: str
    author: str
    year: int


@app.get("/")
def root():
    return {"message": "HELLO WORLD"}


@app.get("/books")
def list_books(db: Session = Depends(get_db)):
    # TODO: return db.query(Book).all()
    return db.query(Book).all()


@app.get("/books/{book_id}")
def get_book(book_id: int, db: Session = Depends(get_db)):
    # TODO: book = db.get(Book, book_id)
    # TODO: nếu book is None → raise HTTPException(status_code=404, detail="Book not found")
    # TODO: return book
    book = db.get(Book, book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@app.post("/books", status_code=201)
def create_book(payload: BookCreate, db: Session = Depends(get_db)):
    # TODO: tạo Book(...), db.add, db.commit, db.refresh, return book
    new_book = Book(
        title=payload.title,
        author=payload.author,
        year=payload.year,
        )
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book

@app.put("/books/{book_id}")
def update_book(book_id: int, payload: BookCreate, db: Session = Depends(get_db)):
    # TODO: lấy book theo id; không có → 404
    # TODO: gán title/author/year từ payload; commit; refresh; return
    book = db.get(Book, book_id)
    if book is None:
        raise HTTPException(status_code=404,detail="Book not found")
    book.title = payload.title
    book.author = payload.author
    book.year = payload.year

    db.commit()
    db.refresh(book)
    return book


@app.delete("/books/{book_id}", status_code=204)
def delete_book(book_id: int, db: Session = Depends(get_db)):
    # TODO: lấy book; không có → 404; db.delete; commit; return None
    book = db.get(Book, book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    db.delete(book)
    db.commit()
    return None