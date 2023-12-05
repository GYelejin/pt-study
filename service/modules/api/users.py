from fastapi import Response, Depends
from uuid import UUID, uuid4

from .base import BaseAPIRouter
from service.modules.models import SessionData
from service.modules.services.users import backend, cookie, verifier


router = BaseAPIRouter(prefix='/user', tags=['user'])


@router.post("/register/{name}")
async def create_session(name: str, response: Response):

    session = uuid4()
    data = SessionData(username=name)

    await backend.create(session, data)
    cookie.attach_to_response(response, session)

    return f"created session for {name}"


@router.get("/whoami", dependencies=[Depends(cookie)])
async def whoami(session_data: SessionData = Depends(verifier)):
    return session_data


@router.post("/delete_session")
async def del_session(response: Response, session_id: UUID = Depends(cookie)):
    await backend.delete(session_id)
    cookie.delete_from_response(response)
    return "deleted session"
