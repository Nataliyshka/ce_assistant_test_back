from playwright.sync_api import expect, Page, Locator
from config import settings


def test_cart(page_authed: Page):
    """
    Тест корзины позитивный
    """
    # Ждём, пока body получит style="overflow: auto;" (прелоадер завершил работу)
    page_authed.wait_for_selector("body[style*='overflow: auto']")
    
    customer_phone = settings.CUSTOMER_GOLD
    page_authed.get_by_label("Телефон покупателя").fill("7" + customer_phone)
    page_authed.locator("button[class*='arrowBtn']").click()
    wait_for_loader(page_authed)

    customer_card = page_authed.locator("div[class*='customer_card']")
    expect(customer_card).to_be_visible()

    # Проверяем имя покупателя - используем структуру документа
    customer_name = customer_card.locator("div[class*='content'] >> p").first
    expect(customer_name).to_be_visible()
    expect(customer_name).not_to_be_empty()

    # Проверяем телефон
    phone = page_authed.locator("p[class*='phone']")
    expect(phone).to_be_visible()
    expect(phone).to_have_text(f"+7 ({customer_phone[:3]}) {customer_phone[3:6]} {customer_phone[6:8]}-{customer_phone[8:]}")

    # Проверяем тип карты
    card_type = page_authed.locator("div[class*='card_type']")
    expect(card_type).to_be_visible()
    expect(card_type.locator("p")).not_to_be_empty()

    # Поиск товара
    page_authed.wait_for_selector("body[style*='overflow: auto']")
    page_authed.get_by_role("button", name="Поиск").click()
    page_authed.get_by_placeholder("Поиск").fill("2000999699450")
    page_authed.get_by_text("Штрихкод: 2000999699450").click()
    page_authed.get_by_role("button", name="Выбрать").click()
    page_authed.wait_for_selector("body[style*='overflow: hidden']")

    # Добавляем ещё один товар
    page_authed.wait_for_selector("body[style*='overflow: auto']")
    page_authed.get_by_role("button", name="Поиск").click()
    page_authed.get_by_placeholder("Поиск").fill("2000999699443")
    page_authed.get_by_text("Штрихкод: 2000999699443").click()
    page_authed.get_by_role("button", name="Выбрать").click()
    page_authed.wait_for_selector("body[style*='overflow: hidden']")
    page_authed.wait_for_selector("body[style*='overflow: auto']")

    cart_items = page_authed.locator("div[class*='product_card']").all()
    assert len(cart_items) == 2, "Неверное количество товаров в корзине"

    # Изменяем количество товара у первого товара
    page_authed.wait_for_selector("body[style*='overflow: auto']")
    item_locator = find_item_locator(page_authed, "Пакет-майка ПНД \"Ценалом\" 28x50, 16мкм")
    item_locator.get_by_role("button", name="Увеличить").click()
    page_authed.wait_for_selector("body[style*='overflow: hidden']")
    page_authed.wait_for_selector("body[style*='overflow: auto']")

    # Проверяем, что количество товара у первого товара увеличилось
    item_locator = find_item_locator(page_authed, "Пакет-майка ПНД \"Ценалом\" 28x50, 16мкм")
    count = item_locator.get_by_label("Значение счетчика").input_value()
    assert count == "2", "Количество товара не увеличилось"

    # Удаляем товар из корзины
    item_locator = find_item_locator(page_authed, "Пакет-майка ПНД \"Ценалом\" 28x50, 16мкм")
    item_locator.locator("button[class*='delete']").click()
    page_authed.wait_for_selector("body[style*='overflow: hidden']")
    page_authed.wait_for_selector("body[style*='overflow: auto']")

    # Проверяем, что количество товаров в корзине уменьшилось
    item_locator = find_item_locator(page_authed, "Пакет-майка ПНД \"Ценалом\" 42x70, 25мкм")
    count = item_locator.get_by_label("Значение счетчика").input_value()
    assert count == "1", "Количество товара не уменьшилось"


    # Применяем бонусы
    customer_card = page_authed.locator("div[class*='customer_card']")
    page_authed.get_by_role("button", name="Списать баллы").click()
    selector_modal = "div[class*='modal_bottom']"
    page_authed.wait_for_selector(selector_modal)
    modal = page_authed.locator(selector_modal)
    modal.locator("button[class*='button']").click()
    wait_for_loader(page_authed)
    
    # Отправка заказа на кассу
    # page_authed.locator("div[class*='modal_menu']").click()
    # page_authed.wait_for_selector("div[class*='content'][class*='open']", state="attached")
    # with page_authed.expect_response("**/api/cart/**/order") as response_info:
    #     page_authed.get_by_role("button", name="Отправить на кассу").click()
    #     response = response_info.value
    #     print(response.json())
    #     assert response.status == 200

    # Оплата по qr-коду
    total_card = page_authed.locator("div[class*='total_card']")
    total_card.get_by_role("button", name="Перейти к оплате").click()
    expect(page_authed.locator("div[class*='qr_image']")).to_be_visible
    page_authed.wait_for_timeout(60000)

    #Получем уведомление об оплате
    page_authed.locator("div[class*='content_nyaef']")
    page_authed.get_by_text("Оплата успешно прошла")
    page_authed.wait_for_timeout(10000)
    


    page_authed.wait_for_timeout(10000)


def wait_for_loader(page: Page):
    # Ждём появления лоадера
    page.wait_for_selector("div[class*='loader'][class*='visible']", state="attached")
    # Ждём исчезновения лоадера
    page.wait_for_selector("div[class*='loader'][class*='visible']", state="detached")

def find_item_locator(page: Page, item_name: str) -> Locator :
    cart_items = page.locator("div[class*='product_card']").all()
    for item_locator in cart_items:
        if item_locator.get_by_text(item_name).is_visible():
            return item_locator
    
    raise Exception(f"Товар {item_name} не найден")


