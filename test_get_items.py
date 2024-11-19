from config import settings

from session import RoleUser, get_session_by_role


def test_get_items():
     s = get_session_by_role(RoleUser.ADMIN)
     