from fastapi import FastAPI, HTTPException
from pydantic import BaseModel 

app = FastAPI()


class Book(BaseModel):
    title: str
    author: str
    year: int
books: dict[int, Book] = {}

@app.get("/books")
def list_books():
    # TODO: trả về danh sách từ dict books
        return books

@app.get("/books/{book_id}")
def get_book(book_id: int):
    # TODO: nếu không có book_id → raise HTTPException(status_code=404, detail="Book not found")
    # TODO: nếu có → trả về book (có thể kèm id)
    if book_id not in books:
         raise HTTPException(status_code=404, detail="Book not found")
    return books[book_id]
 
@app.post("/books", status_code=201)
def create_book(book: Book):
    # TODO: tạo book_id, gán books[book_id] = book, trả về kết quả
    book_id = len(books) + 1
    books[book_id] = book
    return {"id": book_id, **book.model_dump()}

@app.put("/books/{book_id}")
def update_book(book_id: int, book: Book):
    # TODO: kiểm tra book_id tồn tại; cập nhật books[book_id] = 
    if book_id not in books:
         raise HTTPException(status_code=404, detail="Book not found")
    books[book_id] = book
    return {"id": book_id, **book.model_dump()}
 
@app.delete("/books/{book_id}", status_code=204)
def delete_book(book_id: int):
    # TODO: kiểm tra book_id tồn tại; xóa khỏi books; return None
    if book_id not in books:
         raise HTTPException(status_code=404, detail="Book not found")
    del books[book_id]
    return None

   