from fastapi import APIRouter

router = APIRouter(prefix="/service", tags=["service"])


@router.post("/verify")
def verify():
    return {"message": "ok"}
