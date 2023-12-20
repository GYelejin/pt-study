from typing import Annotated, TYPE_CHECKING
import environ 

from fastapi import Depends, UploadFile, File
from dependency_injector.wiring import inject, Provide

from .base import BaseAPIRouter, OctetStream
from service.container import Application
from service.modules.models import SessionData
from service.modules.services.users import cookie, verifier

if TYPE_CHECKING:
    from service.modules.services import FileStorageService


router = BaseAPIRouter(prefix='/files', tags=['files'])

# Configure Minio client
from minio import Minio
env = environ.Env()
minio_client = Minio(
    env("MINIO_HOST"),
    access_key=env("MINIO_ROOT_USER"),
    secret_key=env("MINIO_ROOT_PASSWORD"),
    secure=True
)


@router.get("", dependencies=[Depends(cookie)])
@inject
async def get_files_list(
        session_data: SessionData = Depends(verifier),
        files_service: 'FileStorageService' = Depends(Provide[Application.services.files]),
) -> list[str]:
    # Get the list of files from Minio
    files_list = await files_service.get_files_list(session_data.username)
    return files_list

@router.post("/upload", dependencies=[Depends(cookie)])
@inject
async def upload_file(
        data: Annotated[UploadFile, File()],
        session_data: SessionData = Depends(verifier),
        files_service: 'FileStorageService' = Depends(Provide[Application.services.files]),
) -> None:
    # Save the uploaded file to Minio
    await files_service.upload(session_data.username, data, minio_client)

@router.get("/download/{filename}", dependencies=[Depends(cookie)])
@inject
async def download_file(
        filename: str,
        session_data: SessionData = Depends(verifier),
        files_service: 'FileStorageService' = Depends(Provide[Application.services.files]),
) -> OctetStream:
    # Download the file from Minio
    data = files_service.download(session_data.username, filename, minio_client)
    return OctetStream(
        content=data,
        headers={
            'Content-Disposition': f'attachment; filename="{filename}"',
        }
    )
