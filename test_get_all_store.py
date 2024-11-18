from config import settings
from model.store import StoresRes
from session import RoleUser, get_session_by_role


#получение списка магазинов
def test_get_all_store():
    s = get_session_by_role(RoleUser.ADMIN)
    # 1. Получение списка магазинов
    resp = s.get(settings.BASE_URL + '/api/store')
    response_data = resp.json()
    # Ответ не ' пустой'
    assert response_data is not None, 'Ответ пустой'
    # Соответствует моделе
    validated_stores = StoresRes(**response_data)
    assert len(validated_stores.stores) != 0, 'Список магазинов пустой'
    

    # 2. Не валидный токен
    s.headers['Authorization'] = 'fakeToken'
    negative_resp = s.get(settings.BASE_URL + '/api/store')
    assert negative_resp.status_code >= 400, 'Невалидный токен не вызвал ошибку'

    s.close()
