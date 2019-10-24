"""Модуль для расширения pytest отчетов и запуска маркированных тестов"""
import os
import sys
import pytest


def pytest_addoption(parser):
    """Функция принимает параметр строки -E NAME, где NAME - имя марки теста"""
    parser.addoption(
        "-E",
        action="store",
        metavar="NAME",
        help="only run tests matching the environment NAME."
    )


@pytest.fixture(scope='session', autouse=True)
def configure_report_env(request, environment_info):
    """Фикстура расширяет блок environment_info для html и json отчета"""
    request.config._metadata.update(
        {"Installed Packages": environment_info[0],
         "Envirement_Variables": environment_info[1]})
    request.config._json_environment.append(("Installed Packages", environment_info[0]))
    request.config._json_environment.append(("Envirement_Variables", environment_info[1]))


@pytest.fixture(scope="session")
def environment_info():
    """Фикстура возвращает список установленных пакетов и переменных окружения"""
    return list(sys.modules.keys()), dict(os.environ)


def pytest_configure(config):
    """Функция для регистрации дополнительной марки"""
    config.addinivalue_line("markers", "env(name): mark test to run only on named environment")


def pytest_runtest_setup(item):
    """Функция для определения запускаемых тестов в соответствии с указанной маркой"""
    envnames = [mark.args[0] for mark in item.iter_markers(name='env')]
    if envnames:
        if item.config.getoption("-E") not in envnames:
            pytest.skip("test requires env in %r" % envnames)
