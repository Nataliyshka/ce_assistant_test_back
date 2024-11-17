
from enum import Enum

import requests
from model.auth import AuthRequest, AuthUser

adminUser = AuthUser(username='Цепелева Наталья', password='6vmzmvk8')

class RoleUser(Enum):
    ADMIN = adminUser

def get_session_by_role(role: RoleUser):
    s = requests.Session()

    req = AuthRequest(data=role.value)
    
    resp = s.post('https://login.cenalom.tech/api/v1/auth/login/', json=req.model_dump())
    assert resp.status_code >= 200 and resp.status_code < 400
    response: dict = resp.json()
    assert response.get('accessToken') != None

    s.headers['Authorization'] = f'Bearer {response.get('accessToken')}'

    return s