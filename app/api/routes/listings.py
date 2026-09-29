from __future__ import annotations

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from sqlalchemy import select
from geoalchemy2.functions import ST_DWithin, ST_SetSRID, ST_MakePoint

from app.api.deps import get_db
from app.models.listing import Listing, ListingStatus
from app.models.store import Store
from app.schemas.listing import ListingCreate, ListingOut, ListingUpdate

router = APIRouter(prefix="/listings", tags=["listings"])


@router.get("/", response_model=List[ListingOut])
def list_listings(
    db: Session = Depends(get_db),
    status_filter: Optional[ListingStatus] = Query(default=None, alias="status"),
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
):
    stmt = select(Listing).order_by(Listing.created_at.desc()).limit(limit).offset(offset)
    if status_filter is not None:
        stmt = stmt.where(Listing.status == status_filter)

    return db.execute(stmt).scalars().all()


# ✅ PUT "nearby" BEFORE "/{listing_id}" to avoid route collision
@router.get("/nearby/store/{store_id}", response_model=List[ListingOut])
def nearby_listings_for_store(
    store_id: int,
    radius_m: int = Query(default=3000, ge=50, le=100000),
    db: Session = Depends(get_db),
):
    store = db.get(Store, store_id)
    if not store:
        raise HTTPException(status_code=404, detail="Store not found")

    # ✅ FIX: store.location is a VALUE, so don't call .cast() on it.
    # Use Store.location (column) and store.location (value) directly.
    stmt = (
        select(Listing)
        .join(Store, Listing.store_id == Store.id)
        .where(
            ST_DWithin(
                Store.location.cast("geography"),
                store.location,
                radius_m,
            )
        )
        .order_by(Listing.created_at.desc())
        .limit(200)
    )
    return db.execute(stmt).scalars().all()


@router.get("/nearby", response_model=List[ListingOut])
def nearby_listings_by_point(
    lat: float = Query(..., ge=-90, le=90),
    lon: float = Query(..., ge=-180, le=180),
    radius_m: int = Query(default=3000, ge=50, le=100000),
    db: Session = Depends(get_db),
):
    point = ST_SetSRID(ST_MakePoint(lon, lat), 4326)

    stmt = (
        select(Listing)
        .join(Store, Listing.store_id == Store.id)
        .where(
            ST_DWithin(
                Store.location.cast("geography"),
                point.cast("geography"),
                radius_m,
            )
        )
        .order_by(Listing.created_at.desc())
        .limit(200)
    )
    return db.execute(stmt).scalars().all()


@router.get("/{listing_id}", response_model=ListingOut)
def get_listing(listing_id: int, db: Session = Depends(get_db)):
    listing = db.get(Listing, listing_id)
    if not listing:
        raise HTTPException(status_code=404, detail="Listing not found")
    return listing


@router.post("/", response_model=ListingOut, status_code=status.HTTP_201_CREATED)
def create_listing(payload: ListingCreate, db: Session = Depends(get_db)):
    store = db.get(Store, payload.store_id)
    if not store:
        raise HTTPException(status_code=404, detail="Store not found")

    listing = Listing(
        store_id=payload.store_id,
        title=payload.title,
        description=payload.description,
        price=payload.price,
        category=payload.category,
        status=payload.status,
    )
    db.add(listing)
    db.commit()
    db.refresh(listing)
    return listing


@router.patch("/{listing_id}", response_model=ListingOut)
def update_listing(listing_id: int, payload: ListingUpdate, db: Session = Depends(get_db)):
    listing = db.get(Listing, listing_id)
    if not listing:
        raise HTTPException(status_code=404, detail="Listing not found")

    data = payload.model_dump(exclude_unset=True)
    for k, v in data.items():
        setattr(listing, k, v)

    db.commit()
    db.refresh(listing)
    return listing


@router.delete("/{listing_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_listing(listing_id: int, db: Session = Depends(get_db)):
    listing = db.get(Listing, listing_id)
    if not listing:
        raise HTTPException(status_code=404, detail="Listing not found")

    db.delete(listing)
    db.commit()
    return None