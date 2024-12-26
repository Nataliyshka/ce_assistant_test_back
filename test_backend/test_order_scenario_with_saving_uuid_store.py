from client.assistent.client import AssistantClient
from client.assistent.enum import RoleUser
from client.one_c.client import OneCClient
from config import settings

def test_saving_store():
    """
    Тест проверяет сохранение UUID корзины и данных клиента при работе с разными магазинами.
    Проверяет:
    - Создание корзины с клиентом в первом магазине
    - Создание корзины во втором магазине
    - Сохранение данных первой корзины при переключении между магазинами
    """
    admin_user = RoleUser.ADMIN
    client_assistant = AssistantClient(admin_user)
    client_onec = OneCClient(admin_user)
    store_1 = settings.STORE_ABAKAN
    store_2 = settings.STORE_MINYSINSK

    try:
        # Step 1: Создание корзины в магазине 1 с клиентом
        cart_1 = client_assistant.cart_found_or_create(store_1)
        cart_1 = client_assistant.cart_put_customer_by_phone(cart_1.uuid, settings.CUSTOMER_GOLD)

        assert cart_1.uuid, "Не удалось создать корзину"
        assert cart_1.customer is not None, "Клиент не установлен"

        # Step 2: Создание корзины в магазине 2
        cart_2 = client_assistant.cart_found_or_create(store_2)

        assert cart_2.uuid, "Не удалось создать корзину"

        # Step 3: Проверка, что корзина 1 имеет прежний uuid и клиента

        cart_1_check = client_assistant.cart_found_or_create(store_1)

        assert cart_1_check.uuid == cart_1.uuid, "UUID корзины 1 изменилось"
        assert cart_1_check.customer == cart_1.customer, "Клиент корзины 1 изменился"
        assert cart_1_check.customer.phone == settings.CUSTOMER_GOLD, "Телефон клиента корзины 1 изменился"

        # Step 4: Закрытие корзин
        client_assistant.cart_close(cart_1.uuid)
        client_assistant.cart_close(cart_2.uuid)

        print(cart_1_check.model_dump_json())
    
    finally:
        client_assistant.close_session()
        client_onec.close_session()
