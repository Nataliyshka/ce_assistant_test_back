from playwright.sync_api import expect, Page
from config import settings
from client.assistent.enum import RoleUser

def test_successful_login(page: Page):
    admin = RoleUser.ADMIN

    page.get_by_label("Логин").fill(admin.value.username)
    page.get_by_label("Пароль").fill(admin.value.password)
    page.get_by_role("button", name="Войти").click()
    expect(page).to_have_url(settings.BASE_URL + "/location")
    page.get_by_role("button", name="Да").click()
    expect(page).to_have_url(settings.BASE_URL + "/")


def test_failed_login(page: Page):
    error_user = RoleUser.ERROR

    page.get_by_label("Логин").fill(error_user.value.username)
    page.get_by_label("Пароль").fill(error_user.value.password)
    page.get_by_role("button", name="Войти").click()
    expect(page.get_by_text("Вы ввели неправильный логин или пароль. Попробуйте ещё раз.")).to_be_visible()
