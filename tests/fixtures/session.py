import pytest
from uuid import uuid4

from service.modules.services.users import backend, cookie
from service.modules.models.users import SessionData


@pytest.fixture()
def username_1():
    return 'test'


@pytest.fixture(scope='function')
def user_1_session(username_1):
    session = uuid4()
    backend.data[session] = SessionData(username=username_1)
    yield str(cookie.signer.dumps(session.hex))
    del backend.data[session]
