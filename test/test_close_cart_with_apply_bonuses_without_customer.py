from random import choice
import random

import pytest
from client.assistent.client import AssistantClient
from client.assistent.enum import RoleUser
from client.assistent.model.cart import CartStatus
from client.one_c.client import OneCClient
from config import settings


def test_close_cart_with_apply_bonuses_without_customer():
    admin_user = RoleUser.ADMIN
    client_assistant = AssistantClient(admin_user)
    client_onec = OneCClient(admin_user)
    store = settings.STORE_MINYSINSK

    try:
        initial_cart = client_assistant.cart_found_or_create(store)
        client_assistant.cart_close(initial_cart.uuid)
        current_cart = client_assistant.cart_found_or_create(store)

        items_in_store = client_onec.product_on_store(store)
        items_in_stock = [item for item in items_in_store if item.value > 0]
        rnd_product = choice(items_in_stock)

        current_cart = client_assistant.cart_put_item(
            current_cart.uuid, rnd_product.product
        )

        apply_bonuses = 100

        try:
            current_cart = client_assistant.cart_apply_bonuses(
                current_cart.uuid, apply_bonuses
            )
            pytest.fail("Ожидалась ошибка при применении бонусов без клиента")
        except Exception:
            pass

        client_assistant.cart_close(current_cart.uuid)
        
        new_cart = client_assistant.cart_found_or_create(store)
        assert new_cart.uuid != current_cart.uuid, "Корзина не была закрыта"

    finally:
        client_assistant.close_session()
        client_onec.close_session()
