import pytest
from client.assistent.client import AssistantClient
from client.assistent.enum import RoleUser
from client.assistent.model.cart import CartStatus
from client.one_c.client import OneCClient
from config import settings
from random import choice


def test_sended_cart():
    admin_user = RoleUser.ADMIN
    client_assistant = AssistantClient(admin_user)
    client_onec = OneCClient(admin_user)
    store = settings.STORE_ZHELEZNOGORSK

    try:
        # Закрываем предыдущую корзину и создаем новую
        initial_cart = client_assistant.cart_found_or_create(store)
        client_assistant.cart_close(initial_cart.uuid)
        current_cart = client_assistant.cart_found_or_create(store)
        assert current_cart.uuid, "Не удалось создать корзину"

        # Получаем список товаров в наличии
        items_in_store = client_onec.product_on_store(store)
        items_in_stock = [item for item in items_in_store if item.value > 0]

        # Проверяем, что есть товары в наличии
        assert items_in_stock, "Нет товаров в наличии"

        rnd_product = choice(items_in_stock)

        # Добавляем товар в корзину
        current_cart = client_assistant.cart_put_item(
            current_cart.uuid, rnd_product.product
        )

        try:
            current_cart = client_assistant.cart_order(current_cart.uuid)
            pytest.fail("Ожидалась ошибка при создании заказа с товаром")
        except Exception:
            pass

        # Закрываем корзину и проверяем статус
        client_assistant.cart_close(current_cart.uuid)
        current_cart = client_assistant.cart_get_by_uuid(current_cart.uuid)
        assert current_cart.status == CartStatus.CLOSED, "Корзина не закрыта"

    finally:
        client_assistant.close_session()
        client_onec.close_session()
