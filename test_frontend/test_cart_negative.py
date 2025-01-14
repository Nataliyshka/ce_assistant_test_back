from playwright.sync_api import expect, Page, Locator
from config import settings


def test_cart_negative(page_authed: Page):
    """
    Тест корзины негативный
    """
    # Ждём, пока body получит style="overflow: auto;" (прелоадер завершил работу)
    page_authed.wait_for_selector("body[style*='overflow: auto']")

    

