from pydantic import BaseModel, EmailStr


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str
    name: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str

    class Config:
        from_attributes = True


class TokenPayload(BaseModel):
    sub: str
    type: str
    data: dict
    exp: int

    class Config:
        from_attributes = True


class RefreshTokenRequest(BaseModel):
    refresh_token: str
