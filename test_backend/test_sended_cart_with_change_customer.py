from random import choice, randint
from client.assistent.client import AssistantClient
from client.assistent.enum import RoleUser
from client.assistent.model.cart import CartStatus
from client.one_c.client import OneCClient
from config import settings


def test_sended_cart_with_change_customer():
    admin_user = RoleUser.ADMIN
    client_assistant = AssistantClient(admin_user)
    client_onec = OneCClient(admin_user)
    store = settings.STORE_MINYSINSK

    try:
        initial_cart = client_assistant.cart_found_or_create(store)
        client_assistant.cart_close(initial_cart.uuid)
        current_cart = client_assistant.cart_found_or_create(store)

        current_cart = client_assistant.cart_put_customer_by_phone(current_cart.uuid, settings.CUSTOMER_THREE)
        assert current_cart.customer.is_card_holder, "У клиента нет карты"

        items_in_store = client_onec.product_on_store(store)
        items_in_stock = [item for item in items_in_store if item.value > 0]
        rnd_product = choice(items_in_stock)

        current_cart = client_assistant.cart_put_item(
            current_cart.uuid, rnd_product.product
        )

        assert current_cart, "Товар отсутствует в корзине"
        assert current_cart.items[0].count > 0, "Товар отсутствует на складе"

        apply_bonuses = float(
            randint(0, int(current_cart.customer.total_availible_bonuses))
        )

        current_cart = client_assistant.cart_apply_bonuses(current_cart.uuid, apply_bonuses)
        total_applied_bonuses_by_items = sum(
            item.total_applied_bonuses for item in current_cart.items
        )
        assert (
            current_cart.total_applied_bonuses == total_applied_bonuses_by_items
        ), "Сумма примененных бонусов не соответствует сумме бонусов по товарам"
        calculate_total = (
            current_cart.total_discount_sum - current_cart.total_applied_bonuses
        )
        assert calculate_total == current_cart.total, "Итоговая сумма рассчитана неверно"

        current_cart = client_assistant.cart_delete_customer(current_cart.uuid)
        assert current_cart.customer is None, "Покупатель не удален"

        current_cart = client_assistant.cart_put_customer_by_phone(current_cart.uuid, settings.CUSTOMER_GOLD)
        assert current_cart.customer is not None, "Клиент не установлен"

        client_assistant.cart_order(current_cart.uuid)
        current_cart = client_assistant.cart_get_by_uuid(current_cart.uuid)
        assert current_cart.status == CartStatus.SENDED, "Заказ не отправлен"

        assert current_cart.total_applied_bonuses == 0, "Бонусы предыдущего клиента остались применёнными"
        assert current_cart.total_discount_sum == current_cart.total, "В корзине остались применённые бонусы"

        print(current_cart.model_dump_json())


    finally:
        client_assistant.close_session()
        client_onec.close_session()

        
