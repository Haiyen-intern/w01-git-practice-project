from sqladmin import Admin, ModelView

from app.models import Author, Book


class AuthorAdmin(ModelView, model=Author):
    column_list = [
        Author.id,
        Author.name,
        Author.bio,
        Author.country,
        Author.birth_year,
    ]
    name = "Author"
    name_plural = "Authors"


class BookAdmin(ModelView, model=Book):
    column_list = [Book.id, Book.title, Book.year, Book.summary, Book.author_id]
    name = "Book"
    name_plural = "Books"


def setup_admin(app, engine):
    admin = Admin(app, engine, title="Books Admin")
    admin.add_view(AuthorAdmin)
    admin.add_view(BookAdmin)
    return admin