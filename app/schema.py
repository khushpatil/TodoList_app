from datetime import datetime
from pydantic import BaseModel,EmailStr
from typing import Optional

class Task(BaseModel):
    Task: str
    Status: str = "Not Completed"

class TaskResponse(BaseModel):
    Task_ID: int
    Task: str
    Status: str
    Created_at: datetime

    class Config:
        orm_mode = True

class User(BaseModel):
    Email: EmailStr
    Password: str

class UserResponse(BaseModel):
    User_ID: int
    Email: EmailStr
    Created_at: datetime

    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    Email: EmailStr
    Password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    ID: Optional[str] = None