"""Модуль содержит фикстуры для тестирования базовых типов данных"""
import pytest


@pytest.fixture
def list_fixture(request, begin_module_fixture):
    """Фикстура возаращает список my_list"""
    print("\nTesting begin")
    my_list = [0, 1, 2, 3, 4, 5, 6, 7]

    def fin():
        """Финализатор фикстуры"""
        print("\nTesting finished")

    request.addfinalizer(fin)
    return my_list


@pytest.fixture
def dict_fixture(request, begin_module_fixture):
    """Фикстура возаращает словарь my_dict"""
    print("\nTesting begin")
    my_dict = {"Name": "John", "Surname": "Doe", "Age": 25}

    def fin():
        """Финализатор фикстуры"""
        print("\nTesting finished")

    request.addfinalizer(fin)
    return my_dict


@pytest.fixture
def tuple_fixture(request, begin_module_fixture):
    """Фикстура возаращает кортеж my_dict"""
    print("\nTesting begin")
    my_tuple = ("Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday")

    def fin():
        """Финализатор фикстуры"""
        print("\nTesting finished")

    request.addfinalizer(fin)
    return my_tuple


@pytest.fixture
def set_fixture(request, begin_module_fixture):
    """Фикстура возаращает множество my_set"""
    print("\nTesting begin")
    my_set = {"Red", "Blue", "Green"}

    def fin():
        """Финализатор фикстуры"""
        print("\nTesting finished")

    request.addfinalizer(fin)
    return my_set


@pytest.fixture
def string_fixture(request, begin_module_fixture):
    """Фикстура возаращает строку my_string"""
    print("\nTesting begin")
    my_string = "Hello"

    def fin():
        """Финализатор фикстуры"""
        print("\nTesting finished")

    request.addfinalizer(fin)
    return my_string


@pytest.fixture
def int_fixture(request, begin_module_fixture):
    """Фикстура возаращает целое число my_int"""
    print("\nTesting begin")
    my_int = 17

    def fin():
        """Финализатор фикстуры"""
        print("\nTesting finished")

    request.addfinalizer(fin)
    return my_int


@pytest.fixture(scope="module")
def begin_module_fixture(request, open_session_fixture):
    """Фикстура объявляет тестирование модуля"""
    print("\n==================== Module begin ====================")

    def ended_module_fixture():
        print("\n==================== Module ended ====================")

    request.addfinalizer(ended_module_fixture)


@pytest.fixture(scope="session")
def open_session_fixture(request):
    """Фикстура объявляет открытие сессии"""
    print("\n++++++++++++++++ Test session started ++++++++++++++++")

    def close_session_fixture():
        print("\n++++++++++++++++ Test session closed +++++++++++++++++")

    request.addfinalizer(close_session_fixture)
