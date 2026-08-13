from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base


class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)  # khóa chính
    name: Mapped[str] = mapped_column(String(100), nullable=False)

    books = relationship("Book", back_populates="category")
    