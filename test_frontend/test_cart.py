from playwright.sync_api import expect, Page
from config import settings


def test_cart(page_authed: Page):
    # Ждём, пока body получит style="overflow: auto;" (прелоадер завершил работу)
    page_authed.wait_for_selector("body[style*='overflow: auto']")
    
    customer_phone = settings.CUSTOMER_GOLD
    page_authed.get_by_label("Телефон покупателя").fill("7" + customer_phone)
    page_authed.locator("button[class*='arrowBtn']").click()
    page_authed.wait_for_selector("body[style*='overflow: auto']")

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
    page_authed.get_by_placeholder("Поиск").fill("2008167281322")
    page_authed.get_by_text("Штрихкод: 2008167281322").click()
    page_authed.get_by_role("button", name="Выбрать").click()
    page_authed.wait_for_selector("body[style*='overflow: hidden']")
    page_authed.wait_for_selector("body[style*='overflow: auto']")

    cart_items = page_authed.locator("div[class*='product_card']").all()
    assert len(cart_items) == 2, "Неверное количество товаров в корзине"

    # Изменяем количество товара у первого товара
    page_authed.wait_for_selector("body[style*='overflow: auto']")
    first_product = page_authed.locator("div[class*='product_card']").first
    first_product.get_by_text("Пакет-майка ПНД \"Ценалом\" 42x70, 25мкм").click()
    first_product.get_by_role("button", name="Увеличить").click()
    page_authed.wait_for_selector("body[style*='overflow: hidden']")
    page_authed.wait_for_selector("body[style*='overflow: auto']")

    # Проверяем, что количество товара у первого товара увеличилось
    cart_items = page_authed.locator("div[class*='product_card']").all()
     
    for item_locator in cart_items:
        if item_locator.get_by_text("Пакет-майка ПНД \"Ценалом\" 42x70, 25мкм").is_visible():
            count = item_locator.get_by_label("Значение счетчика").input_value()
            assert count == "2", "Количество товара не увеличилось"
            break

    # Удаляем товар из корзины
    first_product = page_authed.locator("div[class*='product_card']").first
    expect(first_product.get_by_text("Пакет-майка ПНД \"Ценалом\" 42x70, 25мкм")).to_be_visible()
    first_product.locator("button[class*='delete']").click()
    page_authed.wait_for_selector("body[style*='overflow: hidden']")
    page_authed.wait_for_selector("body[style*='overflow: auto']")

    # Проверяем, что количество товаров в корзине уменьшилось
    cart_items = page_authed.locator("div[class*='product_card']").all()

    for item_locator in cart_items:
        if item_locator.get_by_text("Блендер погружной BRAYER BR1243 (800 Вт, 2 скорости, стакан 0,7 л, плавн. рег, венчик, белый").is_visible():
            count = item_locator.get_by_label("Значение счетчика").input_value()
            assert count == "1", "Количество товара не уменьшилось"
            break

    # Применяем бонусы
    customer_card = page_authed.locator("div[class*='customer_card']")
    page_authed.get_by_role("button", name="Списать баллы").click()
    selector_modal = "div[class*='modal_bottom']"
    page_authed.wait_for_selector(selector_modal)
    modal = page_authed.locator(selector_modal)
    modal.locator("button[class*='button']").click()
    page_authed.wait_for_selector("body[style*='overflow: auto']")











    

    page_authed.wait_for_timeout(10000)
