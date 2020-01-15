"""Модуль настройки для теста функциональности Drag'n'Drop для webelement"""
import pytest
from selenium import webdriver
from selenium.webdriver import ChromeOptions, FirefoxOptions


@pytest.fixture(params=["Chrome", "Firefox"])
def browser_driver(request):
    """Фикстура запускает браузеры, переданные в параметрах, и
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
    # Открыть фрейм отдельно, если сайт не открывается
    # web.get("https://marcojakob.github.io/dart-dnd/basic/")
    request.addfinalizer(web.quit)
    return web
