from datetime import datetime

from pydantic import BaseModel


class SessionData(BaseModel):
    username: str


class CreateUserDB(BaseModel):
    username: str


class GetUserDB(BaseModel):
    id: int
    created_at: datetime
    username: str
