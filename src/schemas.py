from typing import List, Optional
from pydantic import BaseModel


class ShowBlog(BaseModel):
    id: str
    title: str

    class Config:
        orm_mode = True

class User(BaseModel):
    id: Optional[str]
    firstname: str
    lastname: str
    email: str
    # blogs: List[ShowBlog] = []

    class Config:
        orm_mode = True


class InsertBlog(BaseModel):
    title: str
    description: Optional[str] = None
    # published: Optional[bool] = True


class Blog(BaseModel):
    id: str
    title: str
    creator: User

    class Config:
        orm_mode = True


# class ShowBlog(Blog):
#     id: Optional[str]

#     class Config():
#         orm_mode = True


class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None
    tags: List[str] = []


class Signup(BaseModel):
    firstname: str
    lastname: str
    email: str
    password: str


class Login(BaseModel):
    email: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None