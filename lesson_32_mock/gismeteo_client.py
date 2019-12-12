"""Клиент для взаимодействия с Gismeteo API"""
import argparse
import json
import requests


def request_current(latitude, longitude, obj_id=None):
    """Функция для запроса текущей погоды по координатам или ID объекта"""
    url = "https://api.gismeteo.net/v2/weather/current/"
    if latitude < -90.0 or latitude > 90.0:
        raise ValueError("Широта должна быть в диапазоне [-90, 90]")
    if longitude < -180.0 or longitude > 180.0:
        raise ValueError("Долгота должна быть в диапазоне [-180, 180]")
    if obj_id and obj_id < 0:
        raise ValueError("ID географического объекта не может быть отрицательным")

    payload = {"latitude": latitude, "longtitude": longitude}
    if obj_id:
        url = url + str(obj_id) + "/"
        payload = None
    response = requests.get(url=url, headers=headers(), params=payload)
    text = json.loads(response.text)
    if response.status_code == 200:
        success_decorator(text)
    else:
        error_decorator(text)
    return response


def success_decorator(text):
    """Функция для обработки полученных данных от успешного запроса"""
    # Здесь происходит какая-то обработка полученных данных
    # При недоступном API результат обработки можно увидеть с использованием Mock"

    print("Запрос обработан.\nКод ответа сервера: 200",
          "\nТип погодных данных:", data_type(text["kind"]),
          "\nДата и время данных:"
          "\nПо стандарту UTC:", text["date"]["UTC"],
          "\nВ формате UNIX по стандарту UTC:", text["date"]["unix"],
          "\nПо локальному времени географического объекта:", text["date"]["local"],
          "\nРазница в минутах между локальным временем "
          "географического объекта и временем по UTC:", text["date"]["time_zone_offset"])


def data_type(kind):
    """Функция возвращает тип погодных данных в зависимости от параметра"""
    # Здесь не дописано возвращение типа "Прогноз"
    if kind == "Obs":
        kind = "Наблюдение"
    return kind


def error_decorator(text):
    """Функция для обработки полученных данных от ошибочного запроса"""
    # Здесь происходит какая-то обработка полученных данных
    # При недоступном API результат обработки можно увидеть с использованием Mock"
    print("Запрос не обработан.\nКод ответа сервера:", text["meta"]["code"],
          "\nТекст сообщения:", text["meta"]["message"])


def get_token():
    """Функция для запроса валидного токена"""
    # Здесь происходит запрос к серверу авторизации,
    # для получения токена по логину и паролю.
    # Сейчас ничего не возвращается
    return None


def headers():
    """Функция для формирования хедеров запроса"""
    # Здесь происходит формирование хедеров для запроса
    # Сейчас ничего не возвращается
    return None


if __name__ == '__main__':

    parser = argparse.ArgumentParser()

    parser.add_argument("--weather", "-w",
                        choices=["current"],
                        action="store",
                        help="Прогноз погоды: "
                             "current - текущая погода",
                        required=True)

    parser.add_argument("--latitude", "-N",
                        action="store",
                        help="Широта",
                        type=float,
                        required=True)

    parser.add_argument("--longtitude", "-E",
                        action="store",
                        help="Долгота",
                        type=float,
                        required=True)

    parser.add_argument("--object_id", "-i",
                        action="store",
                        type=int,
                        help="ID географического объекта")

    arguments = parser.parse_args()

    if arguments.weather == "current":
        s_response = request_current(arguments.latitude, arguments.longtitude, arguments.object_id)
