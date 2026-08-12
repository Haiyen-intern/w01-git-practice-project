from pydantic import BaseModel, Field

class AuthorCreate(BaseModel):
    name: str = Field(min_length=1, max_length=200)
    bio: str | None = Field(default=None, max_length=1000)
    country: str | None = Field(default=None, max_length=100)
    birth_year: int | None = Field(default=None, ge=1000, le=2100)

class AuthorUpdate(BaseModel):
    name: str = Field(min_length=1, max_length=200)
    bio: str | None = Field(default=None, max_length=1000)
    country: str | None = Field(default=None, max_length=100)
    birth_year: int | None = Field(default=None, ge=1000, le=2100)
class AuthorRead(BaseModel):
    id: int
    name: str
    bio: str | None = None
    country: str | None = None
    birth_year: int | None = None

    model_config = {"from_attributes": True}

    
    
    