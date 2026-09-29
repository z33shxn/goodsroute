from __future__ import annotations

from sqlalchemy import Column, Integer, String
from geoalchemy2 import Geometry

from app.database import Base


class Store(Base):
    __tablename__ = "stores"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)

    # SRID 4326 point
    location = Column(Geometry(geometry_type="POINT", srid=4326), nullable=False)
