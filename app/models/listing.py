from __future__ import annotations

import enum
from sqlalchemy import Column, Integer, String, Text, Numeric, Enum, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship

from app.database import Base


class ListingStatus(str, enum.Enum):
    active = "active"
    sold = "sold"
    hidden = "hidden"


class Listing(Base):
    __tablename__ = "listings"

    id = Column(Integer, primary_key=True, index=True)

    store_id = Column(Integer, ForeignKey("stores.id", ondelete="CASCADE"), nullable=False)
    store = relationship("Store")

    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    category = Column(String(100), nullable=True)
    price = Column(Numeric(10, 2), nullable=True)

    status = Column(Enum(ListingStatus, name="listing_status"), nullable=False, default=ListingStatus.active)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)
