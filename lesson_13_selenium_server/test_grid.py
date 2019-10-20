"""Модуль для проверки запуска браузеров на локальной и виртуальной машине"""
import pytest
from selenium import webdriver


@pytest.fixture(params=["firefox", "chrome"])
def web_browser(request):
    """Фикстура запускает браузеры, установленные в параметрах"""
    browser = request.param
    if browser == "chrome":
        driver = webdriver.Remote("http://192.168.1.2:4444/wd/hub", desired_capabilities={
            'browserName': 'chrome', 'version': '', 'platform': 'ANY'})
    elif browser == "firefox":
        driver = webdriver.Remote("http://192.168.1.2:4444/wd/hub", desired_capabilities={
            'browserName': 'firefox', 'version': '', 'platform': 'ANY'})
    else:
        raise Exception(f"{request.param} is not supported!")
    request.addfinalizer(driver.quit)
    return driver


def test_grid(web_browser):
    """Открытие страницы otus.ru и клик на логотипе"""
    web_browser.get("http://otus.ru")
    if "OTUS - Онлайн-образование" not in web_browser.title:
        raise Exception("Unable to load google page!")
    elem = web_browser.find_element_by_class_name("header2__logo-img")
    elem.click()
