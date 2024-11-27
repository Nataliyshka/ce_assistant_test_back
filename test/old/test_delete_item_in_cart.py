from config import settings
from model.cart import CartRes
from session import RoleUser, get_session_by_role


def test_delete_item():
    s = get_session_by_role(RoleUser.ADMIN)
    cart = 'f411b1a8-d9fa-41fb-b437-cfdc0383f7c8'
    find_item = '5bbd5b99-c194-11ea-80c6-a0d3c1ef2117'
    resp = s.delete(settings.BASE_URL + '/api/cart/' + cart + '/item/' + find_item)
    assert resp.status_code >= 200 and resp.status_code < 400, 'Статус код с ошибкой'
    response_data  = resp.json()
    # Ответ не ' пустой'
    assert response_data is not None, 'Ответ пустой'
    # Соответствует моделе
    validated_del_item = CartRes(**response_data)

    s.close()