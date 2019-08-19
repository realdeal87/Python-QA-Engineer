"""В модуле описаны проверки открытого REST API сервиса https://www.openbrewerydb.org/"""
import pytest
import requests


def test_case_1():
    """Из списка пивоварен выводится 20 записей по умолчанию"""
    print("List of breweries: numbers per page is 20")
    res = requests.get("https://api.openbrewerydb.org/breweries").json()
    assert len(res) == 20


def test_case_2():
    """Id пивоварни в запросе совпадает с id в ответе"""
    print("Get a brewery: id777")
    res = requests.get("https://api.openbrewerydb.org/breweries/777").json()
    assert res["id"] == 777


@pytest.mark.parametrize("param", ["id", "name", "brewery_type",
                                   "street", "city", "state", "country"],
                         ids=["id", "name", "brewery_type", "street", "city", "state", "country"])
def test_case_3(param):
    """Ключи присутствуют в записи пивоварни"""
    print("Get a brewery: keys are available")
    res = requests.get("https://api.openbrewerydb.org/breweries/33").json()
    assert param in res


@pytest.mark.parametrize("pages_number, expected_number",
                         [(-1, 20), (0, 0), (1, 1), ("", 20), (50, 50), (51, 50)],
                         ids=["number < 0: 20", "number = 0: 0", "number = 1: 1", "no number: 20",
                              "number = 50: 50", "number > 50: 50"])
def test_case_4(pages_number, expected_number):
    """Граничные значения для количества выводимых записей на странице"""
    print("Pagination & Per Page (default per page is 20; max per page is 50)")
    res = requests.get("https://api.openbrewerydb.org/breweries?page=1&per_page="
                       + str(pages_number)).json()
    assert len(res) == expected_number


def test_case_5():
    """Из списка пивоварен выводится 15 записей по умолчанию в Autocomplete"""
    print("Autocomplete: numbers per page is 15")
    res = requests.get("https://api.openbrewerydb.org/breweries/autocomplete?query=beer").json()
    assert len(res) == 15
