import argparse
import json
import requests


def request_current(latitude, longtitude, id=None):
    url = "https://api.gismeteo.net/v2/weather/current/"
    payload = {"latitude": latitude, "longtitude": longtitude}
    if id:
        url = url + str(id) + "/"
        payload = None
    response = requests.get(url=url, headers=heders(), params=payload)
    text = json.loads(response.text)
    if response.status_code == 200:
        success_decorator(text)
    else:
        error_decorator(text)
    return response


def success_decorator(text):
    print("\nЗапрос обработан.\nКод ответа сервера: 200",
          "\n\nТип погодных данных:", text["kind"],
          "\n\nДата и время данных:"
          "\nПо стандарту UTC:", text["date"]["UTC"],
          "\nВ формате UNIX по стандарту UTC:", text["date"]["unix"],
          "\nПо локальному времени географического объекта:", text["date"]["local"],
          "\nРазница в минутах между локальным временем "
          "географического объекта и временем по UTC:", text["date"]["time_zone_offset"])


def error_decorator(text):
    print("\nЗапрос не обработан.\nКод ответа сервера:", text["meta"]["code"],
          "\nТекст сообщения:", text["meta"]["message"])


def get_token():
    return "56b30cb255.3443075"


def heders():
    return {"X-Gismeteo-Token": get_token(), "Accept-Encoding": "deflate, gzip"}


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
