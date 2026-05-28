from datetime import date, datetime
from pydantic import BaseModel, EmailStr

class PostBase(BaseModel):
    title : str
    content : str
    published : bool
    
class PostCreate(PostBase):
    pass


class PostUpdate(PostBase):
    pass


class PostOut(PostBase):
    id : int
    created_at : datetime

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    email : EmailStr
    password : str
    
class UserOut(BaseModel):
    id : int
    email : EmailStr
    created_at : datetime
    
    class Config:
        orm_mode = True