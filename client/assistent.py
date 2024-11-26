from enum import Enum
import requests
from config import settings
from model.auth import AuthRequest, AuthResponse, AuthUser
from model.cart import Cart, CartRes, PostCartStoreParams
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
            
        assert resp.status_code >= 200 and resp.status_code < 400
        tokens = AuthResponse(**resp.json())

        session.headers['Authorization'] = f'Bearer {tokens.access_token}'
        return session
    
    
    def store_get_all(self) -> list[Store]:
        resp = self.__session.get(self.__base_url + "/api/store")
        validated_resp = StoresRes(**resp.json())
        return validated_resp.stores


    def store_get_by_location(self, lat: float, lon: float) -> Store:
        params = Coordinates(lat=lat, lon=lon)
        resp = self.__session.get(self.__base_url + "/api/store/location", params=params)
        validated_resp = StoreRes(**resp.json())
        return validated_resp.store


    def store_get_by_division(self, division: str) -> Store:
        division = Store(division=division)
        resp = self.__session.get(self.__base_url + "/api/store/division", params=division)
        validated_resp = StoreRes(**resp.json())
        return validated_resp.store
    

    def item_get_all(self, query: str, page: int | None, limit: int | None) -> list[Item]:
        params = GetItemParams(query=query, page=page, limit=limit)
        resp = self.__session.get(self.__base_url + "/api/item", params=params)
        validated_resp = ItemsRes(**resp.json())
        return validated_resp.items
    

    def item_get_by_barcode(self, barcode: str) -> Item:
        barcode = Item(barcodes=barcode)
        resp = self.__session.get(self.__base_url + "/api/barcode/" + barcode)
        validated_resp = ItemRes(**resp.json())
        return validated_resp.item


    def cart_found_or_create(self, store: str) -> Cart:
        params = PostCartStoreParams(store=store)
        resp = self.__session.post(self.__base_url + "/api/cart", params=params)
        validate_resp = CartRes(**resp.json())
        return validate_resp.cart

