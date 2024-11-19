from config import settings
from model.store import Coordinates, StoreRes
from session import RoleUser, get_session_by_role


#Получение магазина по координатам
def test_get_store_location():
    s = get_session_by_role(RoleUser.ADMIN)
    params = Coordinates(lat=56.112929, lon=92.921041)
    # 1 Получение магазина по координатам
    resp = s.get(settings.BASE_URL + '/api/store/location', params=params)
    assert resp.status_code >= 200 and resp.status_code < 400, 'Статус код с ошибкой'
    response_data = resp.json()
    # Ответ не ' пустой'
    assert response_data is not None, 'Ответ пустой'
    # Соответствует моделе
    validated_store_location = StoreRes(**response_data)
    assert validated_store_location.store.coordinates != None , 'Координаты пустые'


    # 2. Не валидный токен
    s.headers['Authorization'] = 'fakeToken'
    negative_resp = s.get(settings.BASE_URL + '/api/store/location')
    assert negative_resp.status_code >= 400, 'Невалидный токен не вызвал ошибку'

    s.close()
