import json
import requests_mock

from gismeteo_client import request_current

with open("answer.json", "r") as file:
    data = file.read()

with requests_mock.mock() as m:
    m.get("https://api.gismeteo.net/v2/weather/current/?latitude=1&longtitude=1", text=data, status_code=200)
    response = request_current(1, 1)
    text = json.loads(response.text)


def test_ok():
    assert len(text["date"]) == 4
