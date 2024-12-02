import requests
from client.one_c.model.order import OrderRes
from client.one_c.model.product import ProductStock
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
        session.auth = (role.value.username, role.value.password)

        return session
    

    def oreder_get_by_cart(self, uuid: str) -> OrderRes:
        resp = self.__session.get(self.__base_url + '/exchange-assistant/V1/order/byCart/' + uuid)
        assert check_status_code(resp.status_code), 'status code is not positive'
        validate_resp = OrderRes(**resp.json())
        return validate_resp
    
    def products_on_store(self, store: str) -> list[ProductStock]:
        resp = self.__session.get
