from client.assistent.client import AssistantClient
from client.assistent.enum import RoleUser
from client.assistent.model.cart import CardType, CartStatus
from client.one_c.client import OneCClient
from config import settings
from random import choice


def test_close_cart():
    """
    Тест проверяет сценарий создания и закрытия корзины с применением бонусов.
    
    Steps:
    1. Создание корзины
    2. Установка клиента
    3. Добавление товаров
    4. Применение бонусов
    5. Закрытие корзины
    """
    admin_user = RoleUser.ADMIN
    client_assistant = AssistantClient(admin_user)
    client_onec = OneCClient(admin_user)
    store = settings.STORE_ZHELEZNOGORSK
    
    try:
        # Step 1: Создание корзины
        initial_cart = client_assistant.cart_found_or_create(store)
        client_assistant.cart_close(initial_cart.uuid)
        current_cart = client_assistant.cart_found_or_create(store)
        assert current_cart.uuid, "Не удалось создать корзину"

        # Step 2: Установка клиента
        current_cart = client_assistant.cart_put_customer_by_phone(
            current_cart.uuid, settings.CUSTOMER_GOLD            
        )
        assert current_cart.customer is not None, "Клиент не установлен"
        assert current_cart.customer.is_card_holder, "У клиента нет карты"
        assert (
            current_cart.customer.card_type == CardType.GOLD
        ), "Тип карты не 'Золотая'"

        # Step 3: Добавление товаров в корзину
        items_by_store = client_onec.product_on_store(store)
        items_in_stock = [item for item in items_by_store if item.value > 0]
        random_item = choice(items_in_stock)
        
        current_cart = client_assistant.cart_put_item(current_cart.uuid, random_item.product)
        assert current_cart.items is not None, "Товар не добавлен в корзину"

        # Step 4: Применение бонусов
        apply_bonuses = float(
            current_cart.customer.total_availible_bonuses + 100
        )
        
        current_cart = client_assistant.cart_apply_bonuses(current_cart.uuid, apply_bonuses)
        current_cart = client_assistant.cart_get_by_uuid(current_cart.uuid)
        print(f"Всего бонусов у клиента: {current_cart.customer.total_balance_bonuses}")
        print(f"Максимально доступно бонусов к списанию в корзине: {current_cart.customer.total_availible_bonuses}")
        print(f"Пытались применить бонусов: {apply_bonuses}")
        actual_applied_bonuses = current_cart.applied_bonuses[0].value if current_cart.applied_bonuses else 0
        print(f"Фактически применено бонусов: {actual_applied_bonuses}")

        # Step 5: Закрытие корзины
        client_assistant.cart_close(current_cart.uuid)
        current_cart = client_assistant.cart_get_by_uuid(current_cart.uuid)
        assert current_cart.status == CartStatus.CLOSED, "Корзина не закрыта"

        print(current_cart.model_dump_json())

    finally:
        client_assistant.close_session()
        client_onec.close_session()


    