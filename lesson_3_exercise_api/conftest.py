"""Модуль содержит функцию и фикстуру для тестирования ответа страницы"""

import pytest
import requests


def pytest_addoption(parser):
    """Функция принимает параметр строки --url или использует значение https://ya.ru по умолчанию"""
    parser.addoption(
        "--url",
        action="store",
        default="https://ya.ru",
        help="This is request url"
    )


@pytest.fixture
def url_param(request):
    """Функция осуществляет запрос по заданному адресу"""
    res = requests.get(request.config.getoption("--url"))
    return res
