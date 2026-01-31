from dataclasses import dataclass

from app.core.settings import settings
from passlib.hash import pbkdf2_sha256  # type: ignore


@dataclass
class PasswordManager:
    @staticmethod
    def _salted_password(password: str) -> str:
        return password + settings.auth.secret_key

    def hash(self, password: str) -> str:
        return pbkdf2_sha256.hash(self._salted_password(password))

    def verify(self, plain_password: str, hashed_password: str) -> bool:
        return pbkdf2_sha256.verify(self._salted_password(plain_password), hashed_password)
