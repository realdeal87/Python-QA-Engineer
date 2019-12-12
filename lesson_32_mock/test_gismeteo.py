"""Модуль для тестирования Gismeteo-клиента с нереализованной функциональностью
и отсутствующим доступом к API сервера на основе Mock-объектов"""
import random
from unittest.mock import patch
import pytest
import requests_mock

from gismeteo_client import request_current, get_token, headers, data_type


@pytest.fixture
def mock():
    """Фикстура создает контекстный менеджер для возвращения объекта Mock"""
    with requests_mock.Mocker() as mock_instance:
        yield mock_instance


@pytest.fixture
def random_coords():
    """Фикстура генерирует тестовые данные - Широту и Долготу"""
    latitude = round(random.uniform(-90, 90), 2)
    longitude = round(random.uniform(-180, 180), 2)
    return latitude, longitude


class TestStatuses:
    """Тесткейсы использующие request_mock для эмуляции доступа к Gismeteo API"""

    def test_status_200(self, mock, random_coords):
        """Возвращение валидного ответа от сервера"""
        lat, lon = random_coords
        print(lat, lon)
        with open("answer.json", "r") as file:
            data = file.read()
        mock.get("https://api.gismeteo.net/v2/weather/current/?latitude="
                 + str(lat) + "&longtitude=" + str(lon), text=data, status_code=200)
        response = request_current(lat, lon)
        assert response.status_code == 200

    def test_bad_token(self, mock, random_coords):
        """Возвращение сообщения о неправильном токене"""
        lat, lon = random_coords
        print(lat, lon)
        mock.get("https://api.gismeteo.net/v2/weather/current/?latitude="
                 + str(lat) + "&longtitude=" + str(lon),
                 text='{"meta": {"code": "404", "message": "Неправильный токен.'
                      'Проверьте заголовок запроса: X-Gismeteo-Token"}}',
                 status_code=404)
        response = request_current(lat, lon)
        assert response.status_code == 404

    def test_wrong_way(self, mock, random_coords):
        """Возвращение сообщения о неправильном адресе запроса"""
        lat, lon = random_coords
        print(lat, lon)
        mock.get("https://api.gismeteo.net/v2/weather/current/?latitude="
                 + str(lat) + "&longtitude=" + str(lon),
                 text='{"meta": {"code": "404", "message": "Неправильный путь.'
                      'Проверьте адрес запроса."}}',
                 status_code=404)
        response = request_current(lat, lon)
        assert response.status_code == 404

    def test_server_err(self, mock, random_coords):
        """Возвращение сообщения об ошибке сервера"""
        lat, lon = random_coords
        print(lat, lon)
        mock.get("https://api.gismeteo.net/v2/weather/current/?latitude="
                 + str(lat) + "&longtitude=" + str(lon),
                 text='{"meta": {"code": "500", "message": "Ошибка сервера.'
                      'Повторите через минуту."}}',
                 status_code=500)
        response = request_current(lat, lon)
        assert response.status_code == 500

    def test_no_money(self, mock, random_coords):
        """Возвращение сообщения о недостаточности средств на счету"""
        lat, lon = random_coords
        print(lat, lon)
        mock.get("https://api.gismeteo.net/v2/weather/current/?latitude="
                 + str(lat) + "&longtitude=" + str(lon),
                 text='{"meta": {"code": "404", "message": "Недостаточно средств на счету."}}',
                 status_code=404)
        response = request_current(lat, lon)
        assert response.status_code == 404

    def test_days_wrong(self, mock, random_coords):
        """Возвращение сообщения о неправильном параметре days"""
        lat, lon = random_coords
        print(lat, lon)
        mock.get("https://api.gismeteo.net/v2/weather/current/?latitude="
                 + str(lat) + "&longtitude=" + str(lon),
                 text='{"meta": {"code": "404", "message": '
                      '"Неправильное значение параметра days"}}',
                 status_code=404)
        response = request_current(lat, lon)
        assert response.status_code == 404


class TestUnits:
    """Тесткейсы использующие unittest.mock для проверки нереализованной функциональности"""

    @patch("gismeteo_client.get_token", return_value="56b30cb255.3443075")
    def test_token(self, get_token):
        """Возвращается валидный токен"""
        assert get_token() == "56b30cb255.3443075"

    @patch("gismeteo_client.headers",
           return_value='{"X-Gismeteo-Token": '
                        '"56b30cb255.3443075", "Accept-Encoding": "deflate, gzip"}")')
    def test_headers(self, headers):
        """Возвращается валидные хедеры"""
        assert headers() == '{"X-Gismeteo-Token": ' \
                            '"56b30cb255.3443075", "Accept-Encoding": "deflate, gzip"}")'

    @patch("gismeteo_client.data_type", return_value="Прогноз")
    def test_data_type(self, get_token):
        """Возвращается тип """
        assert get_token("Frc") == "Прогноз"
