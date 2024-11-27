
from client.assistent import AssistantClient
from session import RoleUser


def test_create_cart_by_store():
    client = AssistantClient(role=RoleUser.ADMIN)
    
    cart_by_store_one = client.cart_found_or_create('test_store_1')
    cart_by_store_two = client.cart_found_or_create('test_store_2')

    cart_by_store_compare = client.cart_found_or_create('test_store_1')

    assert cart_by_store_one.uuid == cart_by_store_compare.uuid, "Ранее созданая корзна на магазине не найдена"
