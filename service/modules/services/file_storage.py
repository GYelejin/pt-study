import aiofiles
import pathlib
from typing import AsyncIterable

from fastapi import UploadFile
from service.config import settings


class FileStorageService:
    chunksize = 1024 * 10

    @staticmethod
    def get_user_dir(username: str):
        user_dir = pathlib.Path(settings.FILES_BASE_PATH) / username
        if not user_dir.exists():
            user_dir.mkdir()
        return user_dir

    async def upload(self, username: str, file: UploadFile) -> None:
        user_dir = self.get_user_dir(username)
        async with aiofiles.open(user_dir / file.filename, mode='w+b') as f:
            await f.write(await file.read())

    async def download(self, username: str, filename: str) -> AsyncIterable[bytes]:
        user_dir = self.get_user_dir(username)
        async with aiofiles.open(user_dir / filename, mode='rb') as f:
            while True:
                data = await f.read(self.chunksize)
                if not data:
                    break
                yield data

    async def get_files_list(self, username: str) -> list[str]:
        user_dir = self.get_user_dir(username)
        return list(i.name for i in user_dir.iterdir())
