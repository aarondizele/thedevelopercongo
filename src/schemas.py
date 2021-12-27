from typing import List, Optional
from pydantic import BaseModel, conint
from uuid import UUID, uuid4
from enum import Enum

class ShowBlog(BaseModel):
    id: str
    title: str

    class Config:
        orm_mode = True

class User(BaseModel):
    id: str
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

class Gender(str, Enum):
    male = "male"
    female = "female"

class Role(str, Enum):
    admin = "admin"
    user = "user"
    student = "student"

class AuthUser(BaseModel):
    id: Optional[UUID] = uuid4()
    firstname: str
    lastname: str
    middlename: Optional[str]
    gender: Gender
    roles: List[Role]

db: List[AuthUser] = [
    AuthUser(
        id=uuid4(),
        firstname="Aaron",
        lastname="Dizele",
        gender=Gender.male,
        roles=[Role.admin, Role.student]
    ),
    AuthUser(
        id=uuid4(),
        firstname="Joanna",
        lastname="Pedro",
        gender=Gender.female,
        roles=[Role.user, Role.student]
    ),
]

class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)
