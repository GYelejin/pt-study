from typing import Any, Optional
from urllib.parse import quote

from pydantic import PostgresDsn, validator, PrivateAttr
from pydantic_settings import BaseSettings
from databases import Database


class DBSettings(BaseSettings):
    postgres_server: str
    postgres_user: str
    postgres_password: str
    postgres_db: str

    sqlalchemy_database_uri: str = ''
    db_escape_char: str = '\\'

    _database: Optional[Database] = PrivateAttr(None)

    @validator('sqlalchemy_database_uri', pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: dict[str, Any]) -> str:  # noqa: U100
        if v and isinstance(v, str):  # pragma: no cover
            return v

        return str(PostgresDsn.build(
            scheme='postgresql',
            username=values['postgres_user'],
            password=quote(values['postgres_password']),
            host=values['postgres_server'],
            path=values["postgres_db"],
        ))

    @property
    def db_obj(self) -> Database:
        if self._database is None:
            self._database = Database(
                self.sqlalchemy_database_uri
            )
        return self._database
