from random import choice
from client.one_c.client import OneCClient
from client.one_c.enum import RoleUser
from config import settings


def test_order_one_c():
    client_onec = OneCClient(role=RoleUser.ADMIN)


    get_order_cart = client_onec.oreder_get_by_cart(uuid='d37619aa-550b-4efb-ba67-0b74dc2322c7')
    print(get_order_cart.model_dump_json())


def test_products_list():
    client_onec = OneCClient(role=RoleUser.ADMIN)

    products_list = client_onec.product_on_store(settings.STORE_ABAKAN)
    
    product_in_stock = [product for product in products_list if product.value > 0]
    rnd_product = choice(product_in_stock)
    print(rnd_product.model_dump_json())
