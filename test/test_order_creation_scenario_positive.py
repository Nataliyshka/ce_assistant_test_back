from random import choice, randint
from client.assistent.client import AssistantClient
from client.assistent.enum import RoleUser
from client.assistent.model.cart import CardType, Cart
from client.assistent.model.item import Item
from client.one_c.client import OneCClient
from config import settings


def test_create_cart():
    """"
        1 Создание корзины
        2 Добавление клиента с клубной картой в корзину
        3 Добавление товара в корзину
        4 Изменение количества одного из товаров
        5 Удаление одного товара из корзины
        6 Применение списания бонусов на товары
        7 Создание заказа в 1С
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

        # Step 2: Добавление клиента с клубной картой в корзину
        current_cart = client_assistant.cart_put_customer_by_phone(current_cart.uuid, settings.CUSTOMER_GOLD)
        assert current_cart.customer is not None, "Клиент не добавлен"
        assert current_cart.customer.is_card_holder, "Клиент не имеет клубной карты"
        assert current_cart.customer.card_type == CardType.GOLD, "Клиент не имеет золотую клубную карту"

        # Step 3: Добавление товара в корзину
        items_in_store = client_onec.product_on_store(store)
        items_in_stock = [item for item in items_in_store if item.value > 3]

        selected_products = set()
        while len(selected_products) < 3:
            rnd_product = choice(items_in_stock)
            selected_products.add(rnd_product.product)

        for product in selected_products:
            current_cart = client_assistant.cart_put_item(
                current_cart.uuid, product
            )
            item_in_cart = get_item_from_cart(product, current_cart)
            assert item_in_cart is not None, f"Товар {product} не добавлен в корзину"
            assert item_in_cart.count > 0, f"Товар {product} отсутствует на складе"

        assert current_cart.items, "Товары не добавлены в корзину"
        assert len(current_cart.items) == 3, "Неверное количество товаров в корзине"

        # Step 4: Изменение количества одного из товаров
     




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

