from config import settings
from model.cart import CartRes
from session import RoleUser, get_session_by_role


def test_put_customer():
    s = get_session_by_role(RoleUser.ADMIN)
    cart='38a8e0ed-5d71-40c8-aa1c-10dad95a51ee'
    phone='9233143623'
    resp = s.put(settings.BASE_URL + '/api/cart/' + cart + '/customer/' + phone)
    assert resp.status_code >= 200 and resp.status_code < 400, 'Статус код с ошибкой'
    response_data = resp.json()
    # Ответ не ' пустой'
    assert response_data is not None, 'Ответ пустой'
    # Соответствует моделе
    validated_put_customer = CartRes(**response_data)

    assert phone == validated_put_customer.cart.customer.phone, 'Номер не совпадает с искомым'


    s.close()