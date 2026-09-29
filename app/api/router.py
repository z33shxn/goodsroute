from fastapi import APIRouter

from app.api.routes.health import router as health_router
from app.api.routes.routes import router as routes_router
from app.api.routes.search import router as search_router
from app.api.routes.listings import router as listings_router
from app.api.routes.stores import router as stores_router

api_router = APIRouter()
api_router.include_router(health_router)
api_router.include_router(routes_router)
api_router.include_router(search_router)
api_router.include_router(stores_router)
api_router.include_router(listings_router)
