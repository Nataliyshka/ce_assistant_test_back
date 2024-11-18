from config import settings
from enum import Enum

import requests
from model.auth import AuthRequest, AuthResponse, AuthUser

admin_user = AuthUser(username=settings.ADMIN_LOGIN, password=settings.ADMIN_PASSWORD)
simple_user = AuthUser(username=settings.SIMPLE_LOGIN, password=settings.SIMPLE_PASSWORD)
error_user = AuthUser(username=settings.FAIL_LOGIN, password=settings.FAIL_PASSWORD)


class RoleUser(Enum):
    ADMIN = admin_user
    SIMPLE = simple_user
    ERROR = error_user

def get_session_by_role(role: RoleUser):
    s = requests.Session()
    req = AuthRequest(data=role.value)
    resp = s.post(settings.BASE_AUTH_URL + '/api/v1/auth/login/', json=req.model_dump())
    
    assert resp.status_code >= 200 and resp.status_code < 400
    
    response: dict = resp.json()
    tokens = AuthResponse(**response)

    assert tokens.access_token != None

    s.headers['Authorization'] = f'Bearer {tokens.access_token}'

    return s