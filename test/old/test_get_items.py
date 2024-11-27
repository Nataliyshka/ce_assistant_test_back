from config import settings
from model.item import GetItemParams, Item, ItemsRes
from session import RoleUser, get_session_by_role

# Получение номенклатуры
def test_get_items():
     s = get_session_by_role(RoleUser.ADMIN)
     # Добавление обязательных / необязательных значений запроса
     params = GetItemParams(query='Sakura', page=None, limit=None)
     resp = s.get(settings.BASE_URL + '/api/item', params=params)
     assert resp.status_code >= 200 and resp.status_code < 400, 'Статус код c ошибкой'
     response_data = resp.json()
     # Ответ не ' пустой'
     assert response_data is not None, 'Ответ пустой'
     # Соответствует моделе
     validate_items = ItemsRes(**response_data)
     assert len(validate_items.items) != 0, 'Товаров не найденно'

     first_item = validate_items.items[0]

     assert params.query.lower() in first_item.title.lower(), 'Заголовок товара не содержит искомое значение'


     s.close()