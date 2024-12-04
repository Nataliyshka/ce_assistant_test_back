from client.assistent.client import AssistantClient
from client.assistent.enum import RoleUser
from client.assistent.model.cart import CardType, CartStatus
from client.one_c.client import OneCClient
from config import settings
from random import choice, randint
import pytest


def test_create_order_negative_item():
    """
    Сценарий проверки создания заказа с товаром, отсутствующим на складе
    
    Шаги:
    1. Создание корзины
    2. Добавление клиента (серебряная карта)
    3. Добавление товаров (один с нулевым остатком)
    4. Применение бонусов
    5. Попытка создания заказа (ожидается ошибка)
    6. Удаление товара с нулевым остатком
    7. Успешное создание заказа
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
        assert current_cart.uuid, "Не удалось создать корзину"

        # Step 2: Добавление клиента в корзину
        current_cart = client_assistant.cart_put_customer_by_phone(
            current_cart.uuid, settings.CUSTOMER_SILVER
        )
        assert current_cart.customer is not None, "Клиент не установлен"
        assert current_cart.customer.is_card_holder, "У клиента нет карты"
        assert (
            current_cart.customer.card_type == CardType.SILVER
        ), "Тип карты не 'Серебряная'"

        # Step 3: Добавление товаров в корзину
        items_by_store = client_onec.product_on_store(store)
        items_in_stock = [item for item in items_by_store if item.value > 0]

        rnd_item_not_null_stock = choice(items_in_stock)
        assert rnd_item_not_null_stock.value > 0, "Товар отсутствует на складе"
        
        # Добавляем товар с нулевым остатком
        current_cart = client_assistant.cart_put_item(current_cart.uuid, settings.NULL_ITEM)
        assert current_cart.items[-1].count == 0, "Товар есть в наличии"
        
        current_cart = client_assistant.cart_put_item(
            current_cart.uuid, rnd_item_not_null_stock.product
        )
     

        # Step 4: Применение бонусов
        apply_bonuses = float(
            randint(0, int(current_cart.customer.total_availible_bonuses))
        )
        # Добавляем проверку на отрицательные бонусы
        assert apply_bonuses >= 0, "Применены отрицательные бонусы"
        assert apply_bonuses <= current_cart.customer.total_availible_bonuses, "Применено больше бонусов, чем доступно"
        current_cart = client_assistant.cart_apply_bonuses(
            current_cart.uuid, apply_bonuses
        )
        total_applied_bonuses_by_items = sum(
            item.total_applied_bonuses for item in current_cart.items
        )
        assert (
            current_cart.total_applied_bonuses == total_applied_bonuses_by_items
        ), "Сумма примененных бонусов не соответствует сумме бонусов по товарам"
        calculate_total = (
            current_cart.total_discount_sum - current_cart.total_applied_bonuses
        )
        assert (
            calculate_total == current_cart.total
        ), "Итоговая сумма рассчитана неверно"

        #Step 5: Создание заказа
        try:
            client_assistant.cart_order(current_cart.uuid)
            pytest.fail("Ожидалась ошибка при создании заказа с отсутствующим товаром")
        except Exception:
            # Продолжаем выполнение теста, так как ошибка ожидаема
            pass
        
        # Проверяем, что статус корзины не изменился
        current_cart = client_assistant.cart_get_by_uuid(current_cart.uuid)
        assert current_cart.status != CartStatus.SENDED, "Заказ не должен быть отправлен"

        # Step 6: Удаление товара из корзины
        serch_null_item_in_cart = next(item for item in current_cart.items if item.count == 0)
        changed_cart = client_assistant.cart_delete_item(current_cart.uuid, serch_null_item_in_cart.guid)
        assert all(item.count > 0 for item in changed_cart.items), "Товар не удален из корзины"

        # Step 7: Отправка корзины
        client_assistant.cart_order(changed_cart.uuid)
        changed_cart = client_assistant.cart_get_by_uuid(changed_cart.uuid)
        assert changed_cart.status == CartStatus.SENDED, "Заказ не отправлен"


        print(changed_cart.model_dump_json())

    finally:
        client_assistant.close_session()
        client_onec.close_session()
