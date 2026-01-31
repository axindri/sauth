from app.core.logger import get_logger
from fastapi import HTTPException

logger = get_logger(__name__)


class NotFoundException(HTTPException):
    def __init__(self, detail: str):
        super().__init__(status_code=404, detail=detail)


class UnauthorizedException(HTTPException):
    def __init__(self, detail: str):
        super().__init__(status_code=401, detail=detail)


class ForbiddenException(HTTPException):
    def __init__(self, detail: str):
        super().__init__(status_code=403, detail=detail)


class BadRequestException(HTTPException):
    def __init__(self, detail: str):
        super().__init__(status_code=400, detail=detail)


class UnexpectedErrorException(HTTPException):
    def __init__(self, detail: str, error: Exception | None = None):
        super().__init__(status_code=500, detail=detail)
        if error:
            logger.error(f"{detail}: {error}")
        else:
            logger.error(detail)
