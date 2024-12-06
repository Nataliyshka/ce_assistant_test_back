import requests
from config import settings
from client.assistent.enum import RoleUser
from client.assistent.model.auth import AuthRequest, AuthResponse
from client.utils import check_status_code
from client.assistent.model.cart import Cart, CartRes, CountItemsReq, OrderRes, PostCartStoreParams
from client.assistent.model.payment import PaymentInfo, PaymentInfoRes, PaymentQrCode
from client.assistent.model.store import Coordinates, Store, StoreRes, StoresRes
from client.assistent.model.item import GetItemParams, Item, ItemRes, ItemsRes



class AssistantClient:
    """Клиент для работы с ассистентом
    """
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
        """Получение списка магазинов.
        Args:
            Нет параметров.

        Returns:
            list[`Store`]: Список магазинов.

        Raises:
            `AssertionError`: Если код ответа от сервера не является успешным.

        """
        resp = self.__session.get(self.__base_url + "/api/store")
        assert check_status_code(resp.status_code), 'status code is not positive'
        validated_resp = StoresRes(**resp.json())
        return validated_resp.stores


    def store_get_by_location(self, lat: float, lon: float) -> Store:
        """Получение магазина по координатам.

        Args:
            lat (`float`): Широта.
            lon (`float`): Долгота.

        Returns:
            `Store`: Магазин.
        """
        params = Coordinates(lat=lat, lon=lon)
        resp = self.__session.get(self.__base_url + "/api/store/location", params=params)
        assert check_status_code(resp.status_code), 'status code is not positive'
        validated_resp = StoreRes(**resp.json())
        return validated_resp.store


    def store_get_by_division(self, division: str) -> Store:
        """Получение магазина по division.

        Args:
            division (`str`): Division магазина.

        Returns:
            `Store`: Магазин.
        """
        params = {'division': division}
        resp = self.__session.get(self.__base_url + "/api/store/division", params=params)
        assert check_status_code(resp.status_code), 'status code is not positive'
        validated_resp = StoreRes(**resp.json())
        return validated_resp.store
    

    def item_get_all(self, query: str, page: int | None, limit: int | None) -> list[Item]:
        """Получение списка товаров.

        Args:
            query (`str`): Поисковый запрос.
            page (`int` | `None`): Номер страницы.
            limit (`int` | `None`): Количество товаров на странице.

        Returns:
            list[`Item`]: Список товаров.
        """
        params = GetItemParams(query=query, page=page, limit=limit)
        resp = self.__session.get(self.__base_url + "/api/item", params=params)
        assert check_status_code(resp.status_code), 'status code is not positive'
        validated_resp = ItemsRes(**resp.json())
        return validated_resp.items
    

    def item_get_by_barcode(self, barcode: str) -> Item:
        """Получение товара по barcode.

        Args:
            barcode (`str`): Barcode товара.

        Returns:
            `Item`: Товар.
        """
        resp = self.__session.get(self.__base_url + "/api/barcode/" + barcode)
        assert check_status_code(resp.status_code), 'status code is not positive'
        validated_resp = ItemRes(**resp.json())
        return validated_resp.item


    def cart_found_or_create(self, store: str) -> Cart:
        """Создание корзины или поиск по магазину.

        Args:
            store (`str`): UUID магазина.

        Returns:
            `Cart`: Корзина.
        """
        params = PostCartStoreParams(store=store)
        resp = self.__session.post(self.__base_url + "/api/cart", params=params)
        assert check_status_code(resp.status_code), 'status code is not positive'
        validate_resp = CartRes(**resp.json())
        return validate_resp.cart


    def cart_get_by_uuid(self, cart: str) -> Cart:
        """Получение корзины по uuid.

        Args:
            cart (`str`): UUID корзины.

        Returns:
            `Cart`: Корзина.
        """
        resp = self.__session.get(self.__base_url + '/api/cart/' + cart)
        assert check_status_code(resp.status_code), 'status code is not positive'
        validated_resp = CartRes(**resp.json())
        return validated_resp.cart


    def cart_apply_bonuses(self, cart: str, bonuses: float) -> Cart:
        """Применение бонусов к корзине.

        Args:
            cart (`str`): UUID корзины.
            bonuses (`float`): Количество бонусов.

        Returns:
            `Cart`: Корзина.
        """
        resp = self.__session.post(self.__base_url + '/api/cart/' + cart + '/apply-bonuses/' + str(bonuses))
        assert check_status_code(resp.status_code), 'status code is not positive'
        validated_resp = CartRes(**resp.json())
        return validated_resp.cart
    

    def cart_close(self, cart: str) -> None:
        """Закрытие корзины.

        Args:
            cart (`str`): UUID корзины.
        """
        resp = self.__session.patch(self.__base_url + '/api/cart/' + cart + '/close')
        assert check_status_code(resp.status_code), 'status code is not positive'
        return 
    

    def cart_order(self, cart: str) -> OrderRes:
        """Создание заказа.

        Args:
            cart (`str`): UUID корзины.

        Returns:
            `OrderRes`: Заказ.
        """
        resp = self.__session.post(self.__base_url + '/api/cart/' + cart + '/order')
        assert check_status_code(resp.status_code), 'status code is not positive'
        validated_resp = OrderRes(**resp.json())
        return validated_resp
    

    def cart_put_customer_by_phone(self, cart: str, phone: int) -> Cart:
        """Добавление клиента в корзину по номеру телефона.

        Args:
            cart (`str`): UUID корзины.
            phone (`int`): Номер телефона.

        Returns:
            `Cart`: Корзина.
        """
        resp = self.__session.put(self.__base_url + '/api/cart/' + cart + '/customer/' + phone)
        assert check_status_code(resp.status_code), 'status code is not positive'
        validated_resp = CartRes(**resp.json())
        return validated_resp.cart
    

    def cart_delete_customer(self, cart: str) -> Cart:
        """Удаление клиента из корзины.

        Args:
            cart (`str`): UUID корзины.

        Returns:
            `Cart`: Корзина.
        """
        resp = self.__session.delete(self.__base_url + '/api/cart/' + cart + '/customer')
        assert check_status_code(resp.status_code), 'status code is not positive'
        validared_resp = CartRes(**resp.json())
        return validared_resp.cart
    

    def cart_put_item(self, cart: str, item: str) -> Cart:
        """Добавление товара в корзину.

        Args:
            cart (`str`): UUID корзины.
            item (`str`): UUID товара.

        Returns:
            `Cart`: Корзина.
        """
        resp = self.__session.put(self.__base_url + '/api/cart/' + cart + '/item/' + item)
        assert check_status_code(resp.status_code), 'status code is not positive'
        validared_resp = CartRes(**resp.json())
        return validared_resp.cart
    

    def cart_delete_item(self, cart: str, item: str) -> Cart:
        """Удаление товара из корзины.

        Args:
            cart (`str`): UUID корзины.
            item (`str`): UUID товара.

        Returns:
            `Cart`: Корзина.
        """
        resp = self.__session.delete(self.__base_url + '/api/cart/' + cart + '/item/' + item)
        assert check_status_code(resp.status_code), 'status code is not positive'
        validared_resp = CartRes(**resp.json())
        return validared_resp.cart
    

    def cart_patch_count_item(self, cart: str, item: str, count: float) -> Cart:
        """Изменение количества товара в корзине.

        Args:
            cart (`str`): UUID корзины.
            item (`str`): UUID товара.
            count (`float`): Количество товара.

        Returns:
            `Cart`: Корзина.
        """
        req = CountItemsReq(count=count)
        resp = self.__session.patch(self.__base_url + '/api/cart/' + cart + '/item/' + item, json=req.model_dump())
        assert check_status_code(resp.status_code), 'status code is not positive'
        validated_resp = CartRes(**resp.json())
        return validated_resp.cart
    

    def cart_create_pay(self, cart: str) -> PaymentQrCode:
        """Создание платежа.

        Args:
            cart (`str`): UUID корзины.

        Returns:
            `PaymentQrCode`: QR-код.
        """
        resp = self.__session.post(self.__base_url + '/api/cart/' + cart + '/pay/create')
        assert check_status_code(resp.status_code), 'status code is not positive'
        validated_resp = PaymentQrCode(**resp.json())
        return validated_resp
    

    def cart_get_status_pay(self, cart: str) -> PaymentInfo:
        """Получение статуса платежа.

        Args:
            cart (`str`): UUID корзины.

        Returns:
            `PaymentInfo`: Статус платежа.
        """
        resp = self.__session.get(self.__base_url + '/api/cart/' + cart + '/pay/status')
        assert check_status_code(resp.status_code), 'status code is not positive'
        validated_resp = PaymentInfoRes(**resp.json())
        return validated_resp.payment_info

    def close_session(self) -> None:
        self.__session.close()
