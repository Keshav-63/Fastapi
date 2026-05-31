from datetime import date, datetime
from typing import Annotated, Optional
from pydantic import BaseModel, EmailStr, Field

#Users
class UserCreate(BaseModel):
    email : EmailStr
    password : str
    
class UserOut(BaseModel):
    id : int
    email : EmailStr
    created_at : datetime
    
    class Config:
        orm_mode = True
        
class UserLogin(BaseModel):
    email : EmailStr
    password : str
    
#Auth
class Token(BaseModel):
    access_token : str
    token_type : str
    
class TokenData(BaseModel):
    id : Optional[str] = None
    
    
#Posts
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
    user_id : int
    created_at : datetime
    user : UserOut

    class Config:
        orm_mode = True
        
class Vote(BaseModel):
    post_id : int
    dir : Annotated[int, Field(strict=True, le=1)]