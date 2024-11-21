from config import settings
from model.cart import CartRes
from session import RoleUser, get_session_by_role


def test_get_cart():
    s = get_session_by_role(RoleUser.ADMIN)
    find_cart = '9d3d9f3f-8dbb-411d-ae34-94a70e99f775'
    resp = s.get(settings.BASE_URL + '/api/cart/' + find_cart)
    assert resp.status_code >= 200 and resp.status_code < 400, "Статус код c ошибкой"
    response_data = resp.json()
    # Ответ не ' пустой'
    assert response_data is not None, "Ответ пустой"
    # Соответствует моделе
    validated_get_cart = CartRes(**response_data)
    