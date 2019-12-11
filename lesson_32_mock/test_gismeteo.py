import pytest
import requests_mock

from gismeteo_client import request_current


@pytest.fixture
def mock():
    with requests_mock.Mocker() as mock_instance:
        yield mock_instance


def test_status_200(mock):
    with open("answer.json", "r") as file:
        data = file.read()
    print(data)
    mock.get("https://api.gismeteo.net/v2/weather/current/?latitude=1&longtitude=1", text=data, status_code=200)
    response = request_current(1, 1)
    assert response.status_code == 200
    return response


def test_foo(mock):
    mock.get("https://api.gismeteo.net/v2/weather/current/?latitude=1&longtitude=1", text='{"meta":'
             ' {"code": "500", "message": "Ошибка сервера. Повторите через минуту."}}', status_code=500)
    response = request_current(1, 1)
    assert response.status_code == 500
