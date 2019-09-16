"""Модуль предустановок для тестирования функциональности Drag'n'Drop"""
import pytest
from selenium import webdriver
from selenium.webdriver import ChromeOptions, FirefoxOptions


@pytest.fixture(params=["Chrome", "Firefox"])
def browser_driver(request):
    """Фикстура запускает браузеры, установленные в параметрах, и
    открывает страницу 'https://code.makery.ch/library/dart-drag-and-drop/'"""
    browser = request.param
    if browser == "Chrome":
        options = ChromeOptions()
        web = webdriver.Chrome(options=options)
    elif browser == "Firefox":
        options = FirefoxOptions()
        web = webdriver.Firefox(options=options)
    else:
        raise Exception(f"{request.param} is not supported!")
    web.maximize_window()
    web.implicitly_wait(10)
    web.get("https://code.makery.ch/library/dart-drag-and-drop/")
    # request.addfinalizer(web.quit)
    return web
