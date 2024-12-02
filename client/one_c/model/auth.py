from pydantic import BaseModel


class AuthUser(BaseModel):
    username: str
    password: str