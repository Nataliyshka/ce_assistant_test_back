from pydantic import BaseModel, Field

class AuthUser(BaseModel):
    username: str
    password: str

class AuthRequest(BaseModel):
    provider: str = Field(default="oneC")
    data: AuthUser

class AuthResponse(BaseModel):
    access_token: str = Field(..., alias='accessToken')
    refresh_token: str = Field(..., alias='refreshToken')

