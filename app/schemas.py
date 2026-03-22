# app/schemas.py
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from app.models import TransactionType


# ── Auth ──────────────────────────────────────────────
class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    email: str
    created_at: datetime

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str


# ── Category ──────────────────────────────────────────
class CategoryCreate(BaseModel):
    name: str


class CategoryResponse(BaseModel):
    id: int
    name: str
    created_at: datetime

    class Config:
        from_attributes = True


# ── Transaction ───────────────────────────────────────
class TransactionCreate(BaseModel):
    type: TransactionType
    category_id: Optional[int] = None
    note: Optional[str] = ""
    amount: float
    date: str


class TransactionUpdate(BaseModel):
    type: Optional[TransactionType] = None
    category_id: Optional[int] = None
    note: Optional[str] = None
    amount: Optional[float] = None
    date: Optional[str] = None


class TransactionResponse(BaseModel):
    id: int
    type: TransactionType
    category_id: Optional[int]
    note: str
    amount: float
    date: str
    created_at: datetime

    class Config:
        from_attributes = True
