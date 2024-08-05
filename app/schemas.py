from ast import List
from datetime import datetime
from typing import Optional
from fastapi.background import P
from pydantic import BaseModel, EmailStr
from pydantic.types import conint


class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime



class UserLogin(BaseModel):
    email: EmailStr
    password: str

class PostBase(BaseModel):
    title: str
    content: str 
    published: bool = True

class PostCreate(PostBase):
    pass

class PostResponse(PostBase):
    id: int
    created_at: datetime
    creator_id: int
    creator: UserResponse


class PostVote(BaseModel):
    Post: PostResponse
    votes: int

    

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None



class Vote(BaseModel):
    post_id: int
    direction: conint(le=1) # type: ignore