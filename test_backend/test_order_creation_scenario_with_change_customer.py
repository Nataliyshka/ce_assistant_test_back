import random
from client.assistent.client import AssistantClient
from client.assistent.enum import RoleUser
from client.one_c.client import OneCClient
from config import settings

# Проблема на стороне 1С нет возможности установить номер телефона клиента,которого нет в БД
def test_change_customer():
    admin_user = RoleUser.ADMIN
    client_assistant = AssistantClient(admin_user)
    client_onec = OneCClient(admin_user)
    store = settings.STORE_ABAKAN

    try:
        # Step 1: Создание корзины
        inital_cart = client_assistant.cart_found_or_create(store)
        client_assistant.cart_close(inital_cart.uuid)
        current_cart = client_assistant.cart_found_or_create(store)
        assert current_cart.uuid, "Не удалось создать корзину"

        # Step 2: Установка клиента
        unathorized_customer = int(''.join([str(random.randint(0, 9)) for _ in range(10)]))
        current_cart = client_assistant.cart_put_customer_by_phone(current_cart.uuid, str(unathorized_customer))
        print(current_cart.model_dump_json())

    finally:
        client_assistant.close_session()
        client_onec.close_session()

