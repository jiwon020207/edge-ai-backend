from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, List

class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserOut(UserBase):
    id: int
    created_at: datetime
    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

class FaceBase(BaseModel):
    label: Optional[str] = None

class FaceCreate(FaceBase):
    image_url: str

class FaceOut(FaceBase):
    id: int
    image_url: str
    created_at: datetime
    class Config:
        orm_mode = True

class ProtectionBase(BaseModel):
    url_pattern: str
    mode: str

class ProtectionCreate(ProtectionBase):
    pass

class ProtectionOut(ProtectionBase):
    id: int
    created_at: datetime
    class Config:
        orm_mode = True
