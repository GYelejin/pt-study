import asyncio
import pathlib
from typing import Generator
from uuid import uuid4

import pytest
import sqlalchemy.exc
import os
from unittest.mock import AsyncMock, patch
from httpx import AsyncClient
from alembic import command
from alembic.config import Config
from sqlalchemy_utils import create_database, drop_database

from service.main import app
from service.config import settings


pytest_plugins = [
    "tests.fixtures.session",
]


@pytest.fixture(scope="session")
def event_loop():
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.stop()
    loop.close()


@pytest.fixture(scope="function")
async def client() -> Generator:
    async with AsyncClient(app=app, base_url="http://test") as c:
        yield c


# @pytest.fixture(scope="session")
# async def db():
#     database = str(uuid4())
#
#     new_settings = settings.DATABASE.__class__(postgres_db=database)
#
#     settings.DATABASE.sqlalchemy_database_uri = new_settings.sqlalchemy_database_uri
#     sync_db_url = settings.DATABASE.sqlalchemy_database_uri.replace("+asyncpg", "")
#     os.environ["TEST"] = "True"
#     # Create empty database:
#     try:
#         create_database(sync_db_url)
#     except sqlalchemy.exc.ProgrammingError:
#         pass
#
#     # Setup alembic and apply migrations:
#     config_path = pathlib.Path() / "scoring_mgr" / "alembic.ini"
#     alembic_config = Config(str(config_path))
#     command.upgrade(alembic_config, "head")
#
#     await new_settings.db_obj.connect()
#
#     # Tests are executed after that:
#     yield new_settings.db_obj
#
#     drop_database(sync_db_url)
#
#     await new_settings.db_obj.disconnect()
#
#
# @pytest.fixture(autouse=True, scope="session")
# def db_patch(db):
#     with patch("scoring_mgr.common.repository.BaseRepository.db", db):
#         yield
