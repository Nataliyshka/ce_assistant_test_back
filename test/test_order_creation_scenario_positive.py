import math
from random import randint, uniform
from client.assistent import AssistantClient
from model.cart import BonusProgram, CardType, Cart, CartStatus, Customer, Item
from session import RoleUser
from config import settings


def test_create_cart_positive():
    client = AssistantClient(role=RoleUser.ADMIN)

    initial_cart = client.cart_found_or_create(settings.STORE_ABAKAN)
    client.cart_close(initial_cart.uuid)
    current_cart = client.cart_found_or_create(settings.STORE_ABAKAN)

    # Проверка на то, что созданная корзина содержит uuid cart
    assert current_cart.uuid

    current_cart = client.cart_put_customer_by_phone(current_cart.uuid, settings.CUSTOMER_GOLD)
    
    # Проверка на то, что клиент установлен в корзину
    assert current_cart.customer is not None, 'Клиент не установлен'
    
    # Проверка, что у клиента действительно есть КК
    assert current_cart.customer.is_card_holder, 'У клиента нет карты'
    
    # Проверка на соответствие типа полученной карты у клиента
    assert current_cart.customer.card_type == CardType.GOLD, 'Тип карты не "Золото"'

    current_cart = client.cart_put_item(current_cart.uuid, settings.ITEM_BLENDER)

    blender_item = get_item_from_cart(settings.ITEM_BLENDER, current_cart)
    assert blender_item, 'Искомого товара нет в корзине'

    assert blender_item.count > 0, 'Товар отсутствует на остатках'

    new_item_count = get_rand_by_max_count(blender_item.max_count)
    current_cart = client.cart_patch_count_item(current_cart.uuid, blender_item.guid, count=new_item_count)
    
    assert current_cart.customer is not None, 'Покупатель не установлен'

    blender_item_updated = get_item_from_cart(blender_item.guid, current_cart)
    assert blender_item_updated, 'Искомого товара нет в корзине'
    
    # Проверка соответствия добавленного количества товара
    assert blender_item_updated.count == new_item_count

    apply_bonuses = float(randint(0, int(current_cart.customer.total_availible_bonuses)))

    current_cart = client.cart_apply_bonuses(current_cart.uuid, apply_bonuses)

    total_applied_bonuses_by_items = sum(item.total_applied_bonuses for item in current_cart.items)

    # Проверка итоговой суммы
    assert current_cart.total_applied_bonuses == total_applied_bonuses_by_items, 'Максимальное применение бонусов у товаров и корзины не соответствует'
    calculate_total = current_cart.total_discount_sum - current_cart.total_applied_bonuses
    assert calculate_total == current_cart.total, 'Итоговая сумма не верна'

    client.cart_order(current_cart.uuid)

    current_cart = client.cart_get_by_uuid(current_cart.uuid)
    assert current_cart.status == CartStatus.SENDED, 'Корзина не отправлена'

    print(current_cart.model_dump_json())

    client.close_session()


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