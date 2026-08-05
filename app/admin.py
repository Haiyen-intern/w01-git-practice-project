from sqladmin import Admin, ModelView
from app.models import Book


class BookAdmin(ModelView, model=Book):
    column_list = [Book.id, Book.title, Book.author, Book.year]

    name = "Book"
    name_plural = "Books"


def setup_admin(app, engine):
    admin = Admin(app, engine, title="Books Admin")
    admin.add_view(BookAdmin)
    return admin