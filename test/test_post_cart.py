from config import settings
from model.cart import CartRes, PostCartStoreParams
from session import RoleUser, get_session_by_role


def test_post_cart():
    s = get_session_by_role(RoleUser.ADMIN)
    params = PostCartStoreParams(store="d9f3be3a-e612-11ec-80cd-1402ec7abf4d")
    resp = s.post(settings.BASE_URL + "/api/cart", params=params)
    assert resp.status_code >= 200 and resp.status_code < 400, "Статус код c ошибкой"
    response_data = resp.json()
    # Ответ не ' пустой'
    assert response_data is not None, "Ответ пустой"
    # Соответствует моделе
    validated_cart = CartRes(**response_data)

