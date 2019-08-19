"""В модуле описаны проверки открытого REST API сервиса https://dog.ceo/dog-api/"""
import pytest
import requests


def test_case_1():
    """Статус сообщения"""
    print("List all breeds - Status: Success")
    res = requests.get("https://dog.ceo/api/breeds/list/all").json()
    assert res["status"] == "success"


def test_case_2():
    """Сравнение количества подпород у двух пород"""
    print("List all breeds - Bulldog has the same number of breeds as mastiff")
    res = requests.get("https://dog.ceo/api/breeds/list/all").json()
    assert len(res["message"]["bulldog"]) == len(res["message"]["mastiff"])


@pytest.mark.parametrize("input_number, expected_number",
                         [(-1, 1), (0, 1), (1, 1), (2, 2), (50, 50), (51, 50)],
                         ids=["number < 0: 1", "number = 0: 1", "number = 1: 1", "number = 2: 2",
                              "number = 50: 50", "number > 50: 50"])
def test_case_3(input_number, expected_number):
    """Граничные значения для количества выводимых фотографий"""
    print("Multiple random images from all dogs collection - number in (1, 50)")
    res = requests.get("https://dog.ceo/api/breeds/image/random/" + str(input_number)).json()
    assert len(res["message"]) == expected_number


def test_case_4():
    """Количестово всех фотографий всех пород собак"""
    print("All the images from a breed, e.g. hound - 1000 images")
    res = requests.get("https://dog.ceo/api/breed/hound/images").json()
    assert len(res["message"]) == 1000


@pytest.mark.parametrize("sub_breed", ["afghan", "basset", "blood", "english", "ibizan", "walker"],
                         ids=["afghan", "basset", "blood", "english", "ibizan", "walker"])
def test_case_5(sub_breed):
    """Проверка включения в породу всех подпород"""
    print("List all sub-breeds - Hound has all available sub-breeds")
    res = requests.get("https://dog.ceo/api/breed/hound/list").json()
    assert sub_breed in res["message"]
