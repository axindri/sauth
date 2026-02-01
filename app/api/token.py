from app.db.db import get_session
from app.schemas import RefreshTokenRequest, TokenResponse
from app.services.token import TokenService, get_token_service
from fastapi import APIRouter, Depends

router = APIRouter(prefix="/token", tags=["token"])


@router.post("/refresh", response_model=TokenResponse)
async def refresh(
    body: RefreshTokenRequest,
    token_service: TokenService = Depends(get_token_service),
):
    async with get_session() as session:
        access_token, refresh_token = await token_service.refresh_tokens(session, body.refresh_token)
    return TokenResponse(access_token=access_token, refresh_token=refresh_token)
