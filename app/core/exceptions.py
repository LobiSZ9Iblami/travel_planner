from fastapi import HTTPException, status, Request


class AlreadyExistsException(HTTPException):
    def __init__(self, detail: str):
        super().__init__(status_code=status.HTTP_409_CONFLICT, detail=detail)


class NotFoundException(HTTPException):
    def __init__(self, detail: str):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)


class BadRequestException(HTTPException):
    def __init__(self, detail: str):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)


class ExternalAPIException(HTTPException):
    def __init__(self, status_code: int, detail):
        self.status_code = status_code
        self.detail = detail
