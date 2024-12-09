from random import choice, randint
from client.assistent.client import AssistantClient
from client.assistent.enum import RoleUser
from client.assistent.model.cart import CardType, Cart, CartStatus
from client.assistent.model.item import Item
from client.one_c.client import OneCClient
from config import settings


def test_batch_create_cart():
    test_count = 40
    success_count = 0
    failed_count = 0
    
    for i in range(test_count):
        print(f"Тест {i+1} из {test_count}")
        try:
            test_create_cart()
            success_count += 1
        except AssertionError as e:
            print(f"Тест не прошел: {str(e)}")
            failed_count += 1
        except Exception as e:
            print(f"Ошибка выполнения: {str(e)}")
            failed_count += 1
    
    print("\nСтатистика тестирования:")
    print(f"Всего тестов: {test_count}")
    print(f"Успешных: {success_count}")
    print(f"Неуспешных: {failed_count}")
    print(f"Процент успешных: {(success_count/test_count)*100:.1f}%")

def test_create_cart():
    """
    1 Создание корзины
    2 Добавление клиента с клубной картой в корзину
    3 Добавление товара в корзину
    4 Применение списания бонусов на товары
    5 Оплата корзины
    6 Проверка статуса оплаты
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
        current_cart = client_assistant.cart_put_customer_by_phone(
            current_cart.uuid, settings.CUSTOMER_GOLD
        )
        assert current_cart.customer is not None, "Клиент не добавлен"
        assert current_cart.customer.is_card_holder, "Клиент не имеет клубной карты"
        assert (
            current_cart.customer.card_type == CardType.GOLD
        ), "Клиент не имеет золотую клубную карту"

        # Step 3: Добавление товара в корзину
        items_in_store = client_onec.product_on_store(store)
        items_in_stock = [item for item in items_in_store if item.value > 0]
        rnd_product = choice(items_in_stock)

        current_cart = client_assistant.cart_put_item(
            current_cart.uuid, rnd_product.product
        )
        item_from_cart = get_item_from_cart(rnd_product.product, current_cart)
        assert item_from_cart, "Товар отсутствует в корзине"
        assert item_from_cart.count > 0, "Товар отсутствует на складе"

        # Step 4: Применение списания бонусов на товары
        apply_bonuses = float(
            randint(0, int(current_cart.customer.total_availible_bonuses))
        )
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

        # Step 5: Оплата корзины
        client_assistant.cart_create_pay(current_cart.uuid)

        # Step 6: Проверка статуса оплаты
        # client_assistant.cart_get_status_pay(current_cart.uuid)
        # current_cart = client_assistant.cart_get_by_uuid(current_cart.uuid)
        # assert current_cart.status == CartStatus.PAID, "Заказ не оплачен"

        # print(current_cart.model_dump_json())

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
    if max_count <= 0:
        raise ValueError("max_count должен быть положительным числом")
    if max_count < 2:
        return max_count

    lower_bound = 2
    upper_bound = int(2 + (max_count / 10) * 2)
    return float(randint(lower_bound, upper_bound))
