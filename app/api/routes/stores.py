from __future__ import annotations

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import select
from geoalchemy2.functions import ST_SetSRID, ST_MakePoint
from geoalchemy2.shape import to_shape

from app.api.deps import get_db
from app.models.store import Store
from app.schemas.store import StoreCreate, StoreOut

router = APIRouter(prefix="/stores", tags=["stores"])


@router.get("/", response_model=List[StoreOut])
def list_stores(db: Session = Depends(get_db)):
    stores = db.execute(select(Store).order_by(Store.id.desc()).limit(200)).scalars().all()
    out: List[StoreOut] = []
    for s in stores:
        p = to_shape(s.location)
        out.append(StoreOut(id=s.id, name=s.name, lat=p.y, lon=p.x))
    return out


@router.post("/", response_model=StoreOut, status_code=status.HTTP_201_CREATED)
def create_store(payload: StoreCreate, db: Session = Depends(get_db)):
    point = ST_SetSRID(ST_MakePoint(payload.lon, payload.lat), 4326)
    store = Store(name=payload.name, location=point)
    db.add(store)
    db.commit()
    db.refresh(store)

    p = to_shape(store.location)
    return StoreOut(id=store.id, name=store.name, lat=p.y, lon=p.x)


@router.get("/{store_id}", response_model=StoreOut)
def get_store(store_id: int, db: Session = Depends(get_db)):
    store = db.get(Store, store_id)
    if not store:
        raise HTTPException(status_code=404, detail="Store not found")
    p = to_shape(store.location)
    return StoreOut(id=store.id, name=store.name, lat=p.y, lon=p.x)
