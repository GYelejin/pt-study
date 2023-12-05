from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from databases.interfaces import Record

from .base import BaseRepo
from service.modules.models import CreateUserDB, GetUserDB
from service.modules.tables import UsersTable

from service.modules.services import FileStorageService


class UsersRepo(BaseRepo):
    @staticmethod
    def _map_get_user_model(repord: Record):
        return GetUserDB(**repord._mapping)

    async def create_user(self, user: CreateUserDB) -> GetUserDB:
        stmt = (
            insert(UsersTable)
            .values({
                UsersTable.username: user.username
            })
            .returning(UsersTable)
        )
        return self._map_get_user_model(await self.db.fetch_one(stmt))

    async def get_user(self, username: str) -> GetUserDB:
        stmt = (
            select(UsersTable)
            .where(
                UsersTable.username == username
            )
        )
        return self._map_get_user_model(await self.db.fetch_one(stmt))
