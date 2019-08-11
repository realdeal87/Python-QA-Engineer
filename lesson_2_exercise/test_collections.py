"""Модуль содержит тест кейсы для коллекций: список, словарь, кортеж, множество"""


def test_case_1(list_fixture):
    """Длина списка"""
    assert len(list_fixture) == 8


def test_case_2(list_fixture):
    """Сумма элементов списка"""
    assert sum(list_fixture) == 28


def test_case_3(dict_fixture):
    """Принадлежность ключа словарю"""
    assert "Age" in dict_fixture.keys()


def test_case_4(dict_fixture):
    """Конкатенация значений элементов словаря"""
    assert dict_fixture["Name"] + " " + dict_fixture["Surname"] == "John Doe"


def test_case_5(tuple_fixture):
    """Возвращение типа данных кортежа"""
    assert isinstance(tuple_fixture, tuple) is True


def test_case_6(tuple_fixture):
    """Минимальное значение элемента кортежа"""
    assert min(tuple_fixture) == "Friday"


def test_case_7(set_fixture):
    """Очистка множества"""
    assert set_fixture.clear() is None


def test_case_8(set_fixture):
    """Принадлежность элемента множеству"""
    assert "Green" in set_fixture
