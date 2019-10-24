"""Образцы для проврки работы с маркированием тестов"""
import pytest


@pytest.mark.env("GroupA")
def test_1():
    """Этот тест с маркой GroupA пройдет успешно"""
    print("\nTest 1 is running...")
    assert True


@pytest.mark.env("GroupA")
def test_2():
    """Этот тест с маркой GroupA упадет"""
    print("\nTest 2 is running...")
    assert False


@pytest.mark.xfail
@pytest.mark.env("GroupA")
def test_3():
    """Этот тест с маркой GroupA не ожидаемо пройдет успешно"""
    print("\nTest 3 is running...")
    assert True


@pytest.mark.xfail
@pytest.mark.env("GroupA")
def test_4():
    """Этот тест с маркой GroupA ожидаемо упадет"""
    print("\nTest 4 is running...")
    assert False


@pytest.mark.skip
@pytest.mark.env("GroupA")
def test_5():
    """Этот тест с маркой GroupA всегда будет пропущен"""
    print("\nTest 5 is running...")
    assert True


@pytest.mark.env("GroupB")
def test_6():
    """Этот тест с маркой GroupB пройдет успешно"""
    print("\nTest 6 is running...")
    assert True


@pytest.mark.env("GroupB")
def test_7():
    """Этот тест с маркой GroupB упадет"""
    print("\nTest 7 is running...")
    assert False


@pytest.mark.xfail
@pytest.mark.env("GroupB")
def test_8():
    """Этот тест с маркой GroupB не ожидаемо пройдет успешно"""
    print("\nTest 8 is running...")
    assert True


@pytest.mark.xfail
@pytest.mark.env("GroupB")
def test_9():
    """Этот тест с маркой GroupB ожидаемо упадет"""
    print("\nTest 9 is running...")
    assert False


@pytest.mark.skip
@pytest.mark.env("GroupB")
def test_10():
    """Этот тест с маркой GroupB всегда будет пропущен"""
    print("\nTest 10 is running...")
    assert True
