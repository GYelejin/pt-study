from typing import Annotated, TYPE_CHECKING

from fastapi import Depends, UploadFile, File
from dependency_injector.wiring import inject, Provide

from .base import BaseAPIRouter, OctetStream
from service.container import Application
from service.modules.models import SessionData
from service.modules.services.users import cookie, verifier

if TYPE_CHECKING:
    from service.modules.services import FileStorageService


router = BaseAPIRouter(prefix='/files', tags=['files'])


@router.get("", dependencies=[Depends(cookie)])
@inject
async def get_files_list(
        session_data: SessionData = Depends(verifier),
        files_service: 'FileStorageService' = Depends(Provide[Application.services.files]),
) -> list[str]:
    return await files_service.get_files_list(session_data.username)


@router.post("/upload", dependencies=[Depends(cookie)])
@inject
async def upload_file(
        data: Annotated[UploadFile, File()],
        session_data: SessionData = Depends(verifier),
        files_service: 'FileStorageService' = Depends(Provide[Application.services.files]),
) -> None:
    await files_service.upload(session_data.username, data)


@router.get("/download/{filename}", dependencies=[Depends(cookie)])
@inject
async def download_file(
        filename: str,
        session_data: SessionData = Depends(verifier),
        files_service: 'FileStorageService' = Depends(Provide[Application.services.files]),
) -> OctetStream:
    data = files_service.download(session_data.username, filename)
    return OctetStream(
        content=data,
        headers={
            'Content-Disposition': f'attachment; filename="{filename}"',
        }
    )
