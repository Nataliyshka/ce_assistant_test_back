from config import settings
from model.item import Item, ItemRes
from session import RoleUser, get_session_by_role


def test_get_item_barcode():
    s = get_session_by_role(RoleUser.ADMIN)
    find_barcode = '2008167281322'
    resp = s.get(settings.BASE_URL + '/api/item/barcode/' + find_barcode)

    assert resp.status_code >= 200 and resp.status_code < 400, 'Статус код c ошибкой'
    response_data = resp.json()
    # Ответ не ' пустой'
    assert response_data is not None, 'Ответ пустой'
    # Соответствует моделе
    validated_item_barcode = ItemRes(**response_data)
    #

    assert find_barcode in validated_item_barcode.item.barcodes, 'Штриходы товара не содержат искомый штрихкод'
            
    s.close()




