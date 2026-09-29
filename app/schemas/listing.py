from __future__ import annotations

from typing import Optional
from pydantic import BaseModel, Field

from app.models.listing import ListingStatus


class ListingCreate(BaseModel):
    store_id: int
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    category: Optional[str] = None
    price: Optional[float] = None
    status: ListingStatus = ListingStatus.active


class ListingUpdate(BaseModel):
    title: Optional[str] = Field(default=None, min_length=1, max_length=200)
    description: Optional[str] = None
    category: Optional[str] = None
    price: Optional[float] = None
    status: Optional[ListingStatus] = None


class ListingOut(BaseModel):
    id: int
    store_id: int
    title: str
    description: Optional[str]
    category: Optional[str]
    price: Optional[float]
    status: ListingStatus

    class Config:
        from_attributes = True
