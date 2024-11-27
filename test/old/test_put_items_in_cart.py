from config import settings
from model.cart import CartRes
from session import RoleUser, get_session_by_role


def test_put_item_in_cart():
    s = get_session_by_role(RoleUser.ADMIN)
    cart = 'f411b1a8-d9fa-41fb-b437-cfdc0383f7c8'
    find_item = '5bbd5b99-c194-11ea-80c6-a0d3c1ef2117'
    resp = s.put(settings.BASE_URL + '/api/cart/' + cart + '/item/' + find_item)
    assert resp.status_code >= 200 and resp.status_code < 400, 'Статус код с ошибкой'
    response_data = resp.json()
    # Ответ не ' пустой'
    assert response_data is not None, 'Ответ пустой'
    # Соответствует моделе
    validated_item_in_cart = CartRes(**response_data)

    is_founded = any(find_item == item.guid for item in validated_item_in_cart.cart.items)
    assert is_founded, 'Номенклатура не совпадает с искомой'

                

    s.close()