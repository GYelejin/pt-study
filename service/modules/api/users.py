from fastapi import Response, Depends
from uuid import UUID, uuid4
from .base import BaseAPIRouter
from service.modules.models import SessionData, SessionBackend
from service.modules.services.users import backend, cookie, verifier


router = BaseAPIRouter(prefix='/user', tags=['user'])
backend = SessionBackend()


@router.post("/register/{name}")
async def create_session(name: str, password: str, response: Response):
    backend.create_user(name, password)
    session = backend.create_session(name)
    cookie.attach_to_response(response, session.id)
    return f"created session for {name}"


@router.get("/whoami", dependencies=[Depends(cookie)])
async def whoami(session_data: SessionData = Depends(verifier)):
    return session_data


@router.post("/delete_session")
async def del_session(response: Response, session_id: UUID = Depends(cookie)):
    backend.delete_session(session_id)
    cookie.delete_from_response(response)
    return "deleted session"
