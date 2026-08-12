from fastapi import Depends, FastAPI, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.admin import setup_admin
from app.database import engine, get_db
from app.models import Author, Book

app = FastAPI(title="Books API")

setup_admin(app, engine)


class AuthorCreate(BaseModel):
    name: str


class AuthorResponse(AuthorCreate):
    id: int

    class Config:
        from_attributes = True


class BookCreate(BaseModel):
    title: str
    year: int
    summary: str | None = None
    author_id: int | None = None


class BookResponse(BookCreate):
    id: int

    class Config:
        from_attributes = True


@app.get("/authors", response_model=list[AuthorResponse])
def list_authors(db: Session = Depends(get_db)):
    return db.query(Author).all()


@app.get("/authors/{author_id}", response_model=AuthorResponse)
def get_author(author_id: int, db: Session = Depends(get_db)):
    author = db.get(Author, author_id)
    if author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return author


@app.post(
    "/authors", response_model=AuthorResponse, status_code=status.HTTP_201_CREATED
)
def create_author(payload: AuthorCreate, db: Session = Depends(get_db)):
    author = Author(name=payload.name)
    db.add(author)
    db.commit()
    db.refresh(author)
    return author


@app.get("/")
def root():
    return {"message": "HELLO WORLD"}


@app.get("/books", response_model=list[BookResponse])
def list_books(db: Session = Depends(get_db)):
    return db.query(Book).all()


@app.get("/books/{book_id}", response_model=BookResponse)
def get_book(book_id: int, db: Session = Depends(get_db)):
    book = db.get(Book, book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")


@app.post("/books", response_model=BookResponse, status_code=status.HTTP_201_CREATED)
def create_book(payload: BookCreate, db: Session = Depends(get_db)):
    if payload.author_id is not None:
        author = db.get(Author, payload.author_id)
        if author is None:
            raise HTTPException(status_code=404, detail="Author not found")
    new_book = Book(
        title=payload.title,
        year=payload.year,
        summary=payload.summary,
        author_id=payload.author_id,
    )
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book


@app.put("/books/{book_id}", response_model=BookResponse)
def update_book(book_id: int, payload: BookCreate, db: Session = Depends(get_db)):
    book = db.get(Book, book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")

    if payload.author_id is not None:
        author = db.get(Author, payload.author_id)
        if author is None:
            raise HTTPException(status_code=404, detail="Author not found")
    book.title = payload.title
    book.year = payload.year
    book.summary = payload.summary
    book.author_id = payload.author_id

    db.commit()
    db.refresh(book)
    return book


@app.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(book_id: int, db: Session = Depends(get_db)):
    book = db.get(Book, book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    db.delete(book)
    db.commit()
    return None
