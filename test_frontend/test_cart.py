import time
from playwright.sync_api import expect, Page
from config import settings


def test_cart(page_authed: Page):
    customer_phone = settings.CUSTOMER_GOLD
    page_authed.get_by_label("Телефон покупателя").fill("7" + customer_phone)
    page_authed.locator("button[class*='arrowBtn']").click()

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
