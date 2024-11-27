from enum import Enum
import requests
from client.utils import check_status_code
from config import settings
from model.auth import AuthRequest, AuthResponse, AuthUser
from model.cart import Cart, CartRes, CountItemsReq, OrderRes, PostCartStoreParams
from model.payment import PaymentInfo, PaymentInfoRes, PaymentQrCode
from model.store import Coordinates, Store, StoreRes, StoresRes
from model.item import GetItemParams, Item, ItemRes, ItemsRes
from session import RoleUser

admin_user = AuthUser(username=settings.ADMIN_LOGIN, password=settings.ADMIN_PASSWORD)
simple_user = AuthUser(username=settings.SIMPLE_LOGIN, password=settings.SIMPLE_PASSWORD)
error_user = AuthUser(username=settings.FAIL_LOGIN, password=settings.FAIL_PASSWORD)


class RoleUser(Enum):
    ADMIN = admin_user
    SIMPLE = simple_user
    ERROR = error_user


class AssistantClient:
    def __init__(self, role: RoleUser) -> None:
        self.__base_url: str = settings.BASE_URL
        self.__base_url_auth: str = settings.BASE_AUTH_URL
        self.__session = self.__get_authed_session(role)

    def __get_authed_session(self, role: RoleUser) -> requests.Session:
        session = requests.Session()
        req = AuthRequest(data=role.value)
        resp = session.post(self.__base_url_auth + '/api/v1/auth/login/', json=req.model_dump())
            
        assert check_status_code(resp.status_code), 'status code is not positive'
        tokens = AuthResponse(**resp.json())

        session.headers['Authorization'] = f'Bearer {tokens.access_token}'
        return session
    
    
    def store_get_all(self) -> list[Store]:
        resp = self.__session.get(self.__base_url + "/api/store")
        assert check_status_code(resp.status_code), 'status code is not positive'
        validated_resp = StoresRes(**resp.json())
        return validated_resp.stores


    def store_get_by_location(self, lat: float, lon: float) -> Store:
        params = Coordinates(lat=lat, lon=lon)
        resp = self.__session.get(self.__base_url + "/api/store/location", params=params)
        assert check_status_code(resp.status_code), 'status code is not positive'
        validated_resp = StoreRes(**resp.json())
        return validated_resp.store


    def store_get_by_division(self, division: str) -> Store:
        params = {'division': division}
        resp = self.__session.get(self.__base_url + "/api/store/division", params=params)
        assert check_status_code(resp.status_code), 'status code is not positive'
        validated_resp = StoreRes(**resp.json())
        return validated_resp.store
    

    def item_get_all(self, query: str, page: int | None, limit: int | None) -> list[Item]:
        params = GetItemParams(query=query, page=page, limit=limit)
        resp = self.__session.get(self.__base_url + "/api/item", params=params)
        assert check_status_code(resp.status_code), 'status code is not positive'
        validated_resp = ItemsRes(**resp.json())
        return validated_resp.items
    

    def item_get_by_barcode(self, barcode: str) -> Item:
        resp = self.__session.get(self.__base_url + "/api/barcode/" + barcode)
        assert check_status_code(resp.status_code), 'status code is not positive'
        validated_resp = ItemRes(**resp.json())
        return validated_resp.item


    def cart_found_or_create(self, store: str) -> Cart:
        params = PostCartStoreParams(store=store)
        resp = self.__session.post(self.__base_url + "/api/cart", params=params)
        assert check_status_code(resp.status_code), 'status code is not positive'
        validate_resp = CartRes(**resp.json())
        return validate_resp.cart


    def cart_get_by_uuid(self, cart: str) -> Cart:
        resp = self.__session.get(self.__base_url + '/api/cart/' + cart)
        assert check_status_code(resp.status_code), 'status code is not positive'
        validated_resp = CartRes(**resp.json())
        return validated_resp.cart


    def cart_apply_bonuses(self, cart: str, bonuses: float) -> Cart:
        resp = self.__session.post(self.__base_url + '/api/cart/' + cart + '/apply-bonuses/' + bonuses)
        assert check_status_code(resp.status_code), 'status code is not positive'
        validated_resp = CartRes(**resp.json())
        return validated_resp.cart
    

    def cart_close(self, cart: str) -> None:
        resp = self.__session.patch(self.__base_url + '/api/cart/' + cart + '/close')
        assert check_status_code(resp.status_code), 'status code is not positive'
        return 
    

    def cart_order(self, cart: str) -> OrderRes:
        resp = self.__session.post(self.__base_url + '/api/cart/' + cart + '/order')
        assert check_status_code(resp.status_code), 'status code is not positive'
        validated_resp = OrderRes(**resp.json())
        return validated_resp
    

    def cart_put_customer_by_phone(self, cart: str, phone: int) -> Cart:
        resp = self.__session.put(self.__base_url + '/api/cart/' + cart + '/customer/' + phone)
        assert check_status_code(resp.status_code), 'status code is not positive'
        validated_resp = CartRes(**resp.json())
        return validated_resp.cart
    

    def cart_delete_customer(self, cart: str) -> Cart:
        resp = self.__session.delete(self.__base_url + '/api/cart/' + cart + '/customer')
        assert check_status_code(resp.status_code), 'status code is not positive'
        validared_resp = CartRes(**resp.json())
        return validared_resp.cart
    

    def cart_put_item(self, cart: str, item: str) -> Cart:
        resp = self.__session.put(self.__base_url + '/api/cart/' + cart + '/item/' + item)
        assert check_status_code(resp.status_code), 'status code is not positive'
        validared_resp = CartRes(**resp.json())
        return validared_resp.cart
    

    def cart_delete_item(self, cart: str, item: str) -> Cart:
        resp = self.__session.delete(self.__base_url + '/api/cart/' + cart + '/item/' + item)
        assert check_status_code(resp.status_code), 'status code is not positive'
        validared_resp = CartRes(**resp.json())
        return validared_resp.cart
    

    def cart_patch_count_item(self, cart: str, item: str, count: float) -> Cart:
        req = CountItemsReq(count=count)
        resp = self.__session.patch(self.__base_url + '/api/cart/' + cart + '/item/' + item, json=req.model_dump())
        assert check_status_code(resp.status_code), 'status code is not positive'
        validated_resp = CartRes(**resp.json())
        return validated_resp.cart
    

    def cart_create_pay(self, cart: str) -> PaymentQrCode:
        resp = self.__session.post(self.__base_url + '/api/cart/' + cart + '/pay/create')
        assert check_status_code(resp.status_code), 'status code is not positive'
        validated_resp = PaymentQrCode(**resp.json())
        return validated_resp
    

    def cart_get_status_pay(self, cart: str) -> PaymentInfo:
        resp = self.__session.get(self.__base_url + '/api/cart/' + cart + '/pay/status')
        assert check_status_code(resp.status_code), 'status code is not positive'
        validated_resp = PaymentInfoRes(**resp.json())
        return validated_resp.payment_info
