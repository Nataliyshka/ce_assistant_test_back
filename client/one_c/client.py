from pydantic import TypeAdapter
import requests
from client.one_c.model.order import Order
from client.one_c.model.product import Product
from config import settings
from enum import Enum
from client.one_c.enum import RoleUser
from client.utils import check_status_code


class OneCClient:
    def __init__(self, role: RoleUser) -> None:
        self.__session = self.__get_authed_session(role)
        self.__base_url: str = settings.BASE_ONEC_URL

    def __get_authed_session(self, role: RoleUser) -> requests.Session:
        session = requests.Session()
        session.auth = (role.value.username.encode("utf-8"), role.value.password.encode("utf-8"))

        return session
    

    def order_get_by_cart(self, uuid: str) -> Order:
        resp = self.__session.get(self.__base_url + '/exchange-assistant/v1/order/byCart/' + uuid)
        assert check_status_code(resp.status_code), 'status code is not positive'
        validate_resp = Order(**resp.json())
        return validate_resp
    
    
    def product_on_store(self, guid: str) -> list[Product]:
        resp = self.__session.get(self.__base_url + '/ExchangeSite/store/' + guid + '/products')
        type_adapter = TypeAdapter(list[Product])
        validate_resp = type_adapter.validate_python(resp.json())
        return validate_resp
    
    def close_session(self) -> None:
        self.__session.close()