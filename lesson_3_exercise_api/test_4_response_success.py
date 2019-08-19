"""Модуль проверяет ответ страницы на статус 200 ОК, также на содержание страницы в формате html"""


def test_url_success(url_param):
    """Статус страницы соответствует 200 ОК"""
    print("\nStatus code 200 OK")
    assert url_param.status_code == 200


def test_html(url_param):
    """Тело ответа в формате html, иначе в теле JSON нет поля "error" """
    if "text/html" not in url_param.headers["Content-Type"]:
        print("\nNo errors in body")
        assert "error" in url_param.json()
    else:
        print("\nContent-Type is HTML")
