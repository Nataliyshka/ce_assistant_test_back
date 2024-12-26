import pytest
from client.assistent.client import AssistantClient
from client.assistent.enum import RoleUser
from client.assistent.model.cart import CartStatus
from client.one_c.client import OneCClient
from config import settings


def test_create_cart_negative():
    """
    1 Создание корзины
    2 Добавление клиента без клубной карты в корзину
    3 Добавление товара в корзину с нулевым остатком на магазине
    4 Применение списания бонусов на товар
    5 Создание заказа в 1С
    6 Закрытие корзины
    """

    admin_user = RoleUser.ADMIN
    client_assistant = AssistantClient(admin_user)
    client_onec = OneCClient(admin_user)
    store = settings.STORE_MINYSINSK

    try:
        # Step 1: Создание корзины
        initial_cart = client_assistant.cart_found_or_create(store)
        client_assistant.cart_close(initial_cart.uuid)
        current_cart = client_assistant.cart_found_or_create(store)

        # Step 2: Добавление клиента без клубной карты в корзину
        current_cart = client_assistant.cart_put_customer_by_phone(
            current_cart.uuid, settings.CUSTOMER_UNAUTHORIZED
        )
        assert current_cart.customer is not None, "Клиент не добавлен в корзину"
        assert (
            current_cart.customer.is_card_holder is False
        ), "Клиент имеет клубную карту"

        # Step 3: Добавление товара в корзину с нулевым остатком на магазине
        current_cart = client_assistant.cart_put_item(
            current_cart.uuid, settings.NULL_ITEM
        )
        assert current_cart.items[0].count == 0, "Товар есть в наличии"

        # Step 4: Применение списания бонусов на товар
        current_cart = client_assistant.cart_apply_bonuses(current_cart.uuid, 100)
        assert (
            current_cart.total_applied_bonuses == 0
        ), "Бонусы применены к товару с нулевым количеством"
        assert current_cart.total == 0, "Сумма не нулевая"

        # Step 5: Создание заказа в 1С
        try:
            client_assistant.cart_order(current_cart.uuid)
            pytest.fail("Ожидалась ошибка при создании заказа")
        except Exception:
            pass
        assert current_cart.status == CartStatus.OPEN, "Заказ отправлен"

        # Step 6: Закрытие корзины
        client_assistant.cart_close(current_cart.uuid)
        current_cart = client_assistant.cart_get_by_uuid(current_cart.uuid)
        assert current_cart.status == CartStatus.CLOSED, "Корзина не закрыта"

        print(current_cart.model_dump_json())

    finally:
        client_assistant.close_session()
        client_onec.close_session()
