from sqladmin import Admin, ModelView

from app.models import Book


class BookAdmin(ModelView, model=Book):
    column_list = [Book.id, Book.title, Book.year, Book.summary]
    name = "Book"
    name_plural = "Books"


def setup_admin(app, engine) -> Admin:
    admin = Admin(app, engine, title="Books Admin")
    admin.add_view(BookAdmin)
    return admin