"""Тест для удаленного запуска на разных браузерах и системах"""


def test_grid(web_browser):
    """Открытие страницы otus.ru и клик на логотипе"""
    web_browser.get("https://otus.ru")
    if "OTUS - Онлайн-образование" not in web_browser.title:
        raise Exception("Unable to load google page!")
    elem = web_browser.find_element_by_class_name("header2__logo-img")
    elem.click()
