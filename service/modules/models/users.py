from datetime import datetime
from argon2 import PasswordHasher
from pydantic import BaseModel


class SessionData(BaseModel):
    username: str


class UserAccount(BaseModel):
    username: str
    password: str


class CreateUserDB(BaseModel):
    username: str


class GetUserDB(BaseModel):
    id: int
    created_at: datetime
    username: str


class SessionBackend:
    def __init__(self):
        self.users = {}
        self.sessions = {}
        self.hasher = PasswordHasher()

    def create_user(self, username: str, password: str):
        hashed_password = self.hasher.hash(password)
        user = UserAccount(username=username, password=hashed_password)
        self.users[username] = user

    def authenticate(self, username: str, password: str) -> bool:
        user = self.users.get(username)
        if user:
            try:
                self.hasher.verify(user.password, password)
                return True
            except:
                pass
        return False

    def create_session(self, username: str):
        session = SessionData(username=username)
        self.sessions[session.id] = session
        return session

    def get_session(self, session_id: str) -> SessionData:
        return self.sessions.get(session_id)
