from __future__ import annotations

from typing import List
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import select
from geoalchemy2.functions import ST_DWithin, ST_SetSRID, ST_MakePoint

from app.api.deps import get_db
from app.models.listing import Listing
from app.models.store import Store
from app.schemas.listing import ListingOut

router = APIRouter(prefix="/search", tags=["search"])


@router.get("/", response_model=List[ListingOut])
def search_nearby(
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
