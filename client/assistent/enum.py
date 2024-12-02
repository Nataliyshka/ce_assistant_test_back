from enum import Enum
from client.assistent.model.auth import AuthUser
from config import settings


admin_user = AuthUser(username=settings.ADMIN_LOGIN, password=settings.ADMIN_PASSWORD)
simple_user = AuthUser(username=settings.SIMPLE_LOGIN, password=settings.SIMPLE_PASSWORD)
error_user = AuthUser(username=settings.FAIL_LOGIN, password=settings.FAIL_PASSWORD)


class RoleUser(Enum):
    ADMIN = admin_user
    SIMPLE = simple_user
    ERROR = error_user
