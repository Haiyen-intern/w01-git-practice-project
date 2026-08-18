from pydantic import BaseModel, Field


class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    password: str = Field(min_length=8, max_length=100)
    role: int = 1  


class UserRead(BaseModel):
    id: int
    username: str
    role: int

    model_config = {"from_attributes": True}


class UserUpdate(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    password: str | None = Field(default=None, min_length=8, max_length=100)
    role: int = 1