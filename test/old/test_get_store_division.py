from config import settings
from model.store import  StoreRes
from session import RoleUser, get_session_by_role


def test_get_store_divivsion():
    s = get_session_by_role(RoleUser.ADMIN)
    find_division = '3d739a92-b28d-11ed-80d2-1402ec7abf4d'
    # Получение магазина по подразделению
    resp = s.get(settings.BASE_URL + '/api/store/division', params={'division': find_division})
    assert resp.status_code >= 200 and resp.status_code < 400, 'Статус код c ошибкой'
    response_data = resp.json()
    # Ответ не ' пустой'
    assert response_data is not None, 'Ответ пустой'
    # Соответствует моделе
    validate_store_division = StoreRes(**response_data)
    assert validate_store_division.store.division == find_division, 'Подрозделение магазина не совподает с искомым'

    # 2. Не валидный токен
    s.headers['Authorization'] = 'fakeToken'
    negative_resp = s.get(settings.BASE_URL + '/api/store/division')
    assert negative_resp.status_code >= 400, 'Невалидный токен не вызвал ошибку'

    s.close()