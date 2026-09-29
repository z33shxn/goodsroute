from fastapi import APIRouter

router = APIRouter(prefix="/routes", tags=["routes"])


@router.get("/")
def routes_root():
    return {"message": "GoodsRoute routes endpoint"}
