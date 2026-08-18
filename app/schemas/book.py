from pydantic import BaseModel, Field


class BookCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    year: int = Field(ge=1000, le=2100)
    summary: str | None = Field(default=None, max_length=500)


class BookUpdate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    year: int = Field(ge=1000, le=2100)
    summary: str | None = Field(default=None, max_length=500)


class BookRead(BaseModel):
    id: int
    title: str
    year: int
    summary: str | None = None
    model_config = {"from_attributes": True}