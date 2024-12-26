from random import randint
from client.assistent.client import AssistantClient
from client.assistent.enum import RoleUser
from client.assistent.model.cart import CardType, Cart, CartStatus, Item
from client.one_c.client import OneCClient
from config import settings
from random import choice



def test_create_cart_positive():
    """
    Позитивный сценарий создания заказа.
    
    Steps:
    1. Создание корзины
    2. Добавление клиента с золотой картой
    3. Добавление товара
    4. Изменение количества товара
    5. Применение бонусов
    6. Создание заказа
    """
    
    # Инициализация клиентов
    admin_user = RoleUser.ADMIN
    client_assistant = AssistantClient(admin_user)
    client_onec = OneCClient(admin_user)
    store = settings.STORE_ABAKAN

    try:
        # Step 1: Создание корзины
        initial_cart = client_assistant.cart_found_or_create(store)
        client_assistant.cart_close(initial_cart.uuid)
        current_cart = client_assistant.cart_found_or_create(store)
        assert current_cart.uuid, "Не удалось создать корзину"


        # Step 2: Добавление клиента
        current_cart = client_assistant.cart_put_customer_by_phone(
            current_cart.uuid, settings.CUSTOMER_GOLD
        )
        assert current_cart.customer is not None, "Клиент не установлен"
        assert current_cart.customer.is_card_holder, "У клиента нет карты"
        assert current_cart.customer.card_type == CardType.GOLD, 'Тип карты не "Золотая"'

        # Step 3: Добавление товара
        items_in_store = client_onec.product_on_store(store)
        items_in_stock = [item for item in items_in_store if item.value > 0]
        rnd_product = choice(items_in_stock)

        current_cart = client_assistant.cart_put_item(
            current_cart.uuid, rnd_product.product
        )
        item_from_cart = get_item_from_cart(rnd_product.product, current_cart)
        assert item_from_cart, "Товар отсутствует в корзине"
        assert item_from_cart.count > 0, "Товар отсутствует на складе"

        # Step 4: Изменение количества товара
        new_item_count = get_rand_by_max_count(item_from_cart.max_count)

        current_cart = client_assistant.cart_patch_count_item(
            current_cart.uuid, item_from_cart.guid, count=new_item_count
        )
        assert current_cart.customer is not None, "Покупатель не установлен"
        item_from_cart_updated = get_item_from_cart(item_from_cart.guid, current_cart)
        assert item_from_cart_updated, "Товар отсутствует в корзине"
        assert (
            item_from_cart_updated.count == new_item_count
        ), "Количество товара не соответствует заданному"

        # Step 5: Применение бонусов
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

        # Step 6: Создание заказа
        client_assistant.cart_order(current_cart.uuid)
        current_cart = client_assistant.cart_get_by_uuid(current_cart.uuid)
        assert current_cart.status == CartStatus.SENDED, "Заказ не отправлен"


        print(current_cart.model_dump_json())

    finally:
        client_assistant.close_session()
        client_onec.close_session()



def get_item_from_cart(itemGuid: str, cart: Cart) -> Item | None:
    # Проверка на наличие товара в корзине
    for item in cart.items:
        if item.guid == itemGuid:
            return item

    # Если товар не найден, возвращаем None
    return None


def get_rand_by_max_count(max_count: float) -> float:
    if max_count < 2:
        return max_count

    lower_bound = 2
    upper_bound = int(2 + (max_count / 10) * 2)
    return float(randint(lower_bound, upper_bound))
