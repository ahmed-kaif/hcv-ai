from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import datetime


# Used when returning full user info
class UserBase(BaseModel):
    id: int
    name: str
    email: EmailStr
    is_admin: bool
    auth_provider: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


# For user creation (email/password)
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str


# For login
class UserLogin(BaseModel):
    email: EmailStr
    password: str


# Public-facing user info (e.g., in /me)
class UserOut(BaseModel):
    id: int
    name: str
    email: EmailStr
    auth_provider: str

    model_config = ConfigDict(from_attributes=True)
