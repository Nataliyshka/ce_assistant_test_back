from config import settings
from model.cart import CartRes
from session import RoleUser, get_session_by_role


def test_delete_cart_customer():
    s = get_session_by_role(RoleUser.ADMIN)
    find_cart = '38a8e0ed-5d71-40c8-aa1c-10dad95a51ee'
    resp = s.delete(settings.BASE_URL + '/api/cart/' + find_cart + '/customer')
    assert resp.status_code >= 200 and resp.status_code < 400, 'Статус код с ошибкой'
    response_data = resp.json()
    # Ответ не ' пустой'
    assert response_data is not None, 'Ответ пустой'
   # Соответствует моделе
    validated_del_customer = CartRes(**response_data)

    s.close()
