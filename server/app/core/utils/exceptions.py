"""Define exceptions to be used on the app."""

from fastapi import HTTPException


class BadRequest(HTTPException):
    """Bad Request exception, status 400"""

    def __init__(
        self, resource: str = "Resource", resource_id=None, detail: str = None
    ):
        message = detail or (
            f"{resource} is invalid or the request was malformed"
            if resource_id is None
            else f"{resource} #{resource_id} is invalid or the request was malformed"
        )
        super().__init__(status_code=400, detail=message)


class NotFound(HTTPException):
    """Not Found exception, status 404"""

    def __init__(
        self, resource: str = "Resource", resource_id=None, detail: str = None
    ):
        message = detail or (
            f"{resource} is invalid or the request was malformed"
            if resource_id is None
            else f"{resource} #{resource_id} is invalid or the request was malformed"
        )
        super().__init__(status_code=400, detail=message)
