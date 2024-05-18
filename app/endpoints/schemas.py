from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


class Post(BaseModel):
    id: int
    title: str 
    content: str 
    published: bool = True
    created_at: datetime
    owner_id: int

    class Config:
        orm_mode = True
  

class PostBase(BaseModel):
    pass 

class PostCreate(BaseModel):
    title: str 
    content: str 
    published: bool = True
    owner_id: int

    
class UserCreate(BaseModel):
    username: str 
    email: EmailStr 
    password: str
    is_active: bool = True
    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    username: str
    email: str
    password: str
    is_active: bool

    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    
    email: str
    password: str
    is_active: bool
    
    class Config:
        from_attributes = True



class UserOut(BaseModel):
    username: str 
    email: EmailStr 
    # password: str
    is_active: bool = True
    
    class Config:
        from_attributes = True

    
class Token(BaseModel):
    access_token: str  
    password: str

class TokenData(BaseModel):
    id: Optional[str] = None
   
