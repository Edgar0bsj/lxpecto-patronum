from fastapi import Request, status
from fastapi.responses import JSONResponse


class ConflitoException(Exception):
    def __init__(self, detail: str):
        self.detail = detail
        self.status_code = 409


class NotFoundException(Exception):
    def __init__(self, detail: str):
        self.detail = detail
        self.status_code = 404


def register_exception_handlers(app):

    @app.exception_handler(ConflitoException)
    async def app_error_handler(request: Request, exc: ConflitoException):
        return JSONResponse(
            status_code=exc.status_code,
            content={"success": False, "detail": exc.detail},
        )

    @app.exception_handler(NotFoundException)
    async def app_error_handler(request: Request, exc: NotFoundException):
        return JSONResponse(
            status_code=exc.status_code,
            content={"success": False, "detail": exc.detail},
        )
