from pydantic import BaseModel, EmailStr
from datetime import datetime


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class PostCreate(PostBase):
    pass


class ShowPost(PostBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


class User(BaseModel):
    email: EmailStr
    password: str
