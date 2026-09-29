from __future__ import annotations

from pydantic import BaseModel, Field


class StoreCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    lat: float = Field(..., ge=-90, le=90)
    lon: float = Field(..., ge=-180, le=180)


class StoreOut(BaseModel):
    id: int
    name: str
    lat: float
    lon: float

    class Config:
        from_attributes = True
