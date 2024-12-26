import pytest
from typing import Generator
from playwright.sync_api import Playwright, Page, BrowserContext
from client.assistent.enum import RoleUser
from config import settings

@pytest.fixture
def context(playwright: Playwright) -> Generator[BrowserContext, None, None]:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context(
        geolocation={"latitude": 56.112929, "longitude": 92.921041},
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

