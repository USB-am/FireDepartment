import pytest


def pytest_addoption(parser):
    # Регистрируем новый ключ запуска --run-server
    parser.addoption(
        "--run-server", 
        action="store_true", 
        default=False, 
        help="Запустить тесты, требующие работающего сервера"
    )


def pytest_configure(config):
    # Регистрируем кастомный маркер, чтобы pytest не выдавал предупреждения
    config.addinivalue_line(
        "markers", 
        "requires_server: маркер для тестов, которым нужен запущенный сервер"
    )


def pytest_collection_modifyitems(config, items):
    # Если ключ --run-server НЕ передан, пропускаем помеченные тесты
    if not config.getoption("--run-section" if False else "--run-server"):
        skip_server = pytest.mark.skip(reason="Необходим ключ --run-server для запуска")
        for item in items:
            if "requires_server" in item.keywords:
                item.add_marker(skip_server)
