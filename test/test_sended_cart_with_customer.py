import pytest
from client.assistent.client import AssistantClient
from client.assistent.enum import RoleUser
from client.assistent.model.cart import CartStatus
from client.one_c.client import OneCClient
from config import settings


def test_sended_cart_with_customer():
    admin_user = RoleUser.ADMIN
    client_assistant = AssistantClient(admin_user)
    client_onec = OneCClient(admin_user)
    store = settings.STORE_MINYSINSK

    try:
        initial_cart = client_assistant.cart_found_or_create(store)
        client_assistant.cart_close(initial_cart.uuid)
        current_cart = client_assistant.cart_found_or_create(store)

        current_cart = client_assistant.cart_put_customer_by_phone(
            current_cart.uuid, settings.CUSTOMER_THREE
        )
        assert current_cart.customer is not None, "Клиент не установлен"

        try:
            current_cart = client_assistant.cart_order(current_cart.uuid)
            pytest.fail("Ожидалась ошибка при создании заказа с клиентом")
        except Exception:
            pass

        client_assistant.cart_close(current_cart.uuid)
        current_cart = client_assistant.cart_get_by_uuid(current_cart.uuid)
        assert current_cart.status == CartStatus.CLOSED, "Корзина не закрыта"

        print(current_cart.model_dump_json())

    finally:
        client_assistant.close_session()
        client_onec.close_session()
