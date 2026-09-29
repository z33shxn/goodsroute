from app.database import Base

# import models so Alembic sees them
from app.models.store import Store  # noqa: F401
from app.models.listing import Listing  # noqa: F401
