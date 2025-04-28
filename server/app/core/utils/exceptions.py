"""Define exceptions to be used on the app."""

from fastapi import HTTPException, status


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
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=message)


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
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=message)


class CredentialsException(HTTPException):
    """Credentials could not be validated"""

    def __init__(self, detail: str = "Could not validate credentials", headers=None):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=detail, headers=headers
        )
