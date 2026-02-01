import time
from dataclasses import dataclass
from uuid import uuid4

import jwt
from app.core.settings import settings

ACCESS_TYPE = "access"
REFRESH_TYPE = "refresh"


@dataclass
class JwtService:
    secret_key: str
    algorithm: str
    access_expire_seconds: int
    refresh_expire_seconds: int

    def _encode(self, sub: str, token_type: str, expire_seconds: int, extra: dict | None = None) -> str:
        now = int(time.time())
        payload = {
            "sub": sub,
            "type": token_type,
            "jti": str(uuid4()),
            "iat": now,
            "exp": now + expire_seconds,
            **(extra or {}),
        }
        return jwt.encode(
            payload,
            self.secret_key,
            algorithm=self.algorithm,
        )

    def create_access_token(self, sub: str, extra: dict | None = None) -> str:
        return self._encode(sub, ACCESS_TYPE, self.access_expire_seconds, extra)

    def create_refresh_token(self, sub: str, extra: dict | None = None) -> str:
        return self._encode(sub, REFRESH_TYPE, self.refresh_expire_seconds, extra)

    def create_pair(self, sub: str, extra: dict | None = None) -> tuple[str, str]:
        access = self.create_access_token(sub, extra)
        refresh = self.create_refresh_token(sub, extra)
        return access, refresh

    def decode(self, token: str) -> dict:
        return jwt.decode(
            token,
            self.secret_key,
            algorithms=[self.algorithm],
        )


def get_jwt_service() -> JwtService:
    return JwtService(
        secret_key=settings.auth.secret_key,
        algorithm=settings.auth.algorithm,
        access_expire_seconds=settings.auth.access_token_expire_seconds,
        refresh_expire_seconds=settings.auth.refresh_token_expire_seconds,
    )
