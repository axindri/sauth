from fastapi import APIRouter

router = APIRouter(prefix="/token", tags=["token"])


@router.post("/refresh")
def refresh():
    return {"message": "ok"}
