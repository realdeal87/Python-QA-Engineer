"""В модуле описаны проверки открытого REST API сервиса https://jsonplaceholder.typicode.com/"""
import pytest
import requests


def test_case_1():
    """Id поста в запросе совпадает с id в ответе"""
    print("Post is available: id77")
    res = requests.get("https://jsonplaceholder.typicode.com/posts/77").json()
    assert res["id"] == 77


@pytest.mark.parametrize("param", ["userId", "id", "title", "body"],
                         ids=["userId", "id", "title", "body"])
def test_case_2(param):
    """Ключи присутствуют в записи поста"""
    print("Post: keys are available")
    res = requests.get("https://jsonplaceholder.typicode.com/posts/77").json()
    assert param in res

@pytest.mark.parametrize("param", ["name", "email", "body"],
                         ids=["name", "email", "body"])
def test_case_3(param):
    """Тип в параметрах name, email и body тип данных string"""
    print("Comments: params have class string")
    res = requests.get("https://jsonplaceholder.typicode.com/posts/1/comments").json()
    # print(res)
    assert isinstance(res[0][param], str)


def test_case_4():
    """У пользователя 10 постов"""
    print("UserId7 has 10 posts")
    res = requests.get("https://jsonplaceholder.typicode.com/posts?userId=1").json()
    assert len(res) == 10


def test_case_5():
    """Количество фотографий"""
    print("5000 photos available")
    res = requests.get("https://jsonplaceholder.typicode.com/photos").json()
    assert len(res) == 5000
