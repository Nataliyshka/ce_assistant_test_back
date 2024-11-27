from config import settings
from model.cart import CartRes
from session import RoleUser, get_session_by_role


def test_apply_bonuses():
    s = get_session_by_role(RoleUser.ADMIN)
    cart = 'f411b1a8-d9fa-41fb-b437-cfdc0383f7c8'
    bonuses = 399
    resp = s.post(settings.BASE_URL + '/api/cart/' + cart + '/apply-bonuses/' + bonuses)
    assert resp.status_code >= 200 and resp.status_code > 400, 'Статус код с ошибкой'
    response_data = resp.json()

    assert response_data is not None, 'Ответ пустой'

    validated_apply_bonuses = CartRes(**response_data)