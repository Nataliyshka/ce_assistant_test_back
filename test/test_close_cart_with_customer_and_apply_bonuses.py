import random
import pytest
from client.assistent.enum import RoleUser
from client.assistent.client import AssistantClient
from client.assistent.model.cart import CartStatus
from client.one_c.client import OneCClient
from config import settings

# Проблема на стороне 1С нет возможности установить номер телефона клиента,которого нет в БД
def test_close_cart_with_customer_and_apply_bonuses():
    admin_user = RoleUser.ADMIN
    client_assistant = AssistantClient(admin_user)
    client_onec = OneCClient(admin_user)
    store = settings.STORE_MINYSINSK

    try:
        initial_cart = client_assistant.cart_found_or_create(store)
        client_assistant.cart_close(initial_cart.uuid)
        current_cart = client_assistant.cart_found_or_create(store)

        unregistered_customer = int(''.join([str(random.randint(0, 9)) for _ in range(10)]))
        current_cart = client_assistant.cart_put_customer_by_phone(current_cart.uuid, str(unregistered_customer))
        assert current_cart.customer is not None, "Клиент не установлен"

        items_in_store = client_onec.product_on_store(store)
        items_in_stock = [item for item in items_in_store if item.value > 0]
        rnd_product = random.choice(items_in_stock)

        current_cart = client_assistant.cart_put_item(
            current_cart.uuid, rnd_product.product
        )

        apply_bonuses = float(
            random.randint(0, int(current_cart.customer.total_availible_bonuses))
        )

        try:
            current_cart = client_assistant.cart_apply_bonuses(current_cart.uuid, apply_bonuses)
            pytest.fail("Ожидалась ошибка при применении бонусов")
        except Exception:
            pass

        current_cart = client_assistant.cart_close(current_cart.uuid)
        assert current_cart.status == CartStatus.CLOSED, "Корзина не закрыта"


    finally:
        client_assistant.close_session()
        client_onec.close_session()


