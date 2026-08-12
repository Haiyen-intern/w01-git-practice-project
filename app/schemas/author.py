from pydantic import BaseModel, Field


class AuthorBase(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=200)
    bio: str | None = Field(default=None, max_length=1000)
    country: str | None = Field(default=None, max_length=100)
    birth_year: int | None = Field(default=None, ge=1000, le=2100)


class AuthorCreate(AuthorBase):
    name: str = Field(min_length=1, max_length=200)


class AuthorUpdate(AuthorBase):
    name: str | None = Field(default=None, min_length=1, max_length=200)


class AuthorRead(AuthorBase):
    id: int
    name: str

    model_config = {"from_attributes": True}
