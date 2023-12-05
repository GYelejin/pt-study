from fastapi import FastAPI

from .container import Application
import service.modules.api
import service.modules.services
from service.config import settings
from service.modules.api import (
    files_router, users_router,
)


def create_app() -> FastAPI:
    application = Application()
    application.init_resources()
    application.wire(
        packages=[
            service.modules.api,
            service.modules.services,
        ]
    )

    app = FastAPI(
        title=settings.PROJECT_NAME,
        description=f"API for {settings.PROJECT_NAME}",
        version="0.1.0",
        debug=settings.DEBUG,
    )

    app.container = application
    app.include_router(files_router)
    app.include_router(users_router)

    return app


app = create_app()


@app.on_event("startup")
async def startup_event():
    await settings.DATABASE.db_obj.connect()


@app.on_event("shutdown")
async def shutdown() -> None:
    await settings.DATABASE.db_obj.disconnect()
