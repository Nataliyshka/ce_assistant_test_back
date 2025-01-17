import pytest
from typing import Generator
from playwright.sync_api import Playwright, Page, BrowserContext
from client.assistent.client import AssistantClient
from client.assistent.enum import RoleUser
from config import settings

@pytest.fixture
def context(playwright: Playwright) -> Generator[BrowserContext, None, None]:
    browser = playwright.chromium.launch(headless=False)

    admin = RoleUser.ADMIN
    client_assistant = AssistantClient(admin)
    store = client_assistant.store_get_by_location(lat=56.112929, lon=92.921041)
    cart_old = client_assistant.cart_found_or_create(store.guid)
    client_assistant.cart_close(cart_old.uuid)

    context = browser.new_context(
        geolocation={"latitude": store.coordinates.lat, "longitude": store.coordinates.lon},
        permissions=["geolocation"]
    )
    yield context
    context.close()
    browser.close()

@pytest.fixture
def page(context: BrowserContext) -> Generator[Page, None, None]:
    page = context.new_page()

    page.goto(settings.BASE_URL)
    yield page
    page.close()

@pytest.fixture
def page_authed(page: Page):
    admin = RoleUser.ADMIN

    page.get_by_label("Логин").fill(admin.value.username)
    page.get_by_label("Пароль").fill(admin.value.password)
    page.get_by_role("button", name="Войти").click()
    page.get_by_role("button", name="Да").click()

    yield page

