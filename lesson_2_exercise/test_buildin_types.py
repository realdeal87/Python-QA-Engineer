"""Модуль содержит тест кейсы для типов данных: строка и целое число"""


def test_case_1(string_fixture):
    """Конкатенация строк"""
    assert string_fixture + " World!" == "Hello World!"


def test_case_2(string_fixture):
    """Преобразование букв строки в заглавные"""
    assert string_fixture.upper() == "HELLO"


def test_case_3(int_fixture):
    """Остаток при делении"""
    assert int_fixture % 2 == 1


def test_case_4(int_fixture):
    """Возведение в степень"""
    assert pow(int_fixture, 3) == 4913
