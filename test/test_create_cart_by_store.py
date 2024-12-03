
#from client.assistent.client import AssistantClient


# def test_create_cart_by_store():
#     client = AssistantClient(role=RoleUser.ADMIN)
    
#     cart_by_store_one = client.cart_found_or_create('test_store_1')
#     cart_by_store_two = client.cart_found_or_create('test_store_2')

#     cart_by_store_compare = client.cart_found_or_create('test_store_1')

#     assert cart_by_store_one.uuid == cart_by_store_compare.uuid, "Ранее созданая корзна на магазине не найдена"



#     client.cart_close(create_cart.uuid)
#     closed_cart = client.cart_get_by_uuid(create_cart.uuid)
#     assert closed_cart.status == CartStatus.CLOSED, 'Корзина не закрыта'