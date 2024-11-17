import pydantic
import requests
import pytest
from model.store import StoresRes
from session import RoleUser, get_session_by_role


#получение списка магазинов
def test_get_all_store():
    baseUrl = 'https://stage-assistant.cenalom.tech'
    s = get_session_by_role(RoleUser.ADMIN)
    # 1. Получение списка магазинов
    resp = s.get(baseUrl + '/api/store')
    response_data = resp.json()
    # Ответ не пустой
    assert response_data is not None
    # Соответствует моделе
    validated_response = StoresRes(**response_data)
    

    # 2. Не валидный токен
    s.headers.update('Authorization', 'fakeToken')
    negative_resp = s.get('https://stage-assistant.cenalom.tech/api/store')
    assert negative_resp.status_code >= 400

    # Список магазинов из ответа
    stores = response_data.get('stores', [])
    # Получен список
    assert isinstance(stores, list), f'Ожидался список, но получен: {type(stores)}'
    print(stores)
    s.close()
