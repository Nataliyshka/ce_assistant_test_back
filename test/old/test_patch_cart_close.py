from config import settings
from session import RoleUser, get_session_by_role


def test_cart_close():
    s = get_session_by_role(RoleUser.ADMIN)
    find_cart = '9d3d9f3f-8dbb-411d-ae34-94a70e99f775'
    resp = s.patch(settings.BASE_URL + '/api/cart/' + find_cart + '/close')
    assert resp.status_code == 200, "Статус код c ошибкой"


    s.close()



