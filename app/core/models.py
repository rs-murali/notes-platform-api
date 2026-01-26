from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional

class UserCreate(BaseModel):
    name: str = Field(..., max_length=50)
    email: EmailStr

    
class UserUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=50)
    email: Optional[EmailStr] = None

class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr

    class Config:
        from_attributes = True

class NoteCreate(BaseModel):    
    title: str = Field(..., max_length=100)
    content: str
    tags: Optional[list[str]] = None

class NoteUpdate(BaseModel):
    title: Optional[str] = Field(None, max_length=100)
    content: Optional[str] = None
    tags: Optional[list[str]] = None

class NoteResponse(BaseModel):
    id: int
    title: str
    content: str
    tags: Optional[list[str]] = None
    user_id: int

class Note(BaseModel):
    id: int
    title: str
    content: str
    tags: Optional[list[str]]
    user_id: int
    class Config:
        from_attributes = True
        
class User(BaseModel):
    id: int
    name: str
    email: EmailStr
    class Config:
        from_attributes = True