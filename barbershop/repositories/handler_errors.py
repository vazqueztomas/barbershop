from fastapi import HTTPException


class NotFoundResponse(HTTPException):
    detail: str
    status_code: int = 404
