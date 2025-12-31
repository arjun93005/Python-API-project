from symtable import Class
from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


#Schema for Pydantic Model
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class Create_Post(PostBase):
    pass

class Post(PostBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class User_Create(BaseModel):
    email: EmailStr
    password: str

class User(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True

class User_Login(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[int] = None


