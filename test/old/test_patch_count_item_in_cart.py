from config import settings
from model.cart import CartRes, CountItemsReq
from session import RoleUser, get_session_by_role


def test_patch_item():
    s = get_session_by_role(RoleUser.ADMIN)
    req = CountItemsReq(count=1)
    cart = 'f411b1a8-d9fa-41fb-b437-cfdc0383f7c8'
    find_item = '32ee2992-a71a-11ea-80c5-a0d3c1ef2117'
    resp = s.patch(settings.BASE_URL + '/api/cart/' + cart + '/item/' + find_item, json=req.model_dump())
    assert resp.status_code >= 200 and resp.status_code < 400, 'Статус код с ошибкой'
    response_data = resp.json()
    # Ответ не ' пустой'
    assert response_data is not None, 'Ответ пустой'
    # Соответствует моделе
    validated_count_items = CartRes(**response_data)

    s.close()