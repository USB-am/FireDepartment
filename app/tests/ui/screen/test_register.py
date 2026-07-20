import pytest

from ui.screen.register.register_controller import RegisterController as RC


# @pytest.fixture
# def mock_view(mocker):
#     return mocker.MagicMock()

# @pytest.fixture
# def mock_api_client(mocker):
#     return mocker.MagicMock()

# @pytest.fixture
# def mock_model(mocker):
#     return mocker.MagicMock()

# @pytest.fixture
# def register_controller(mocker, mock_view, mock_api_client, mock_model):
#     mocker.patch('ui.screen.register.register_model.RegisterModel', return_value=mock_model)
#     mocker.patch('service.token.AccessTokenManager')
#     return RC(view=mock_view, api_client=mock_api_client)


from unittest.mock import MagicMock, patch


@pytest.fixture
def register_controller(mocker):
    """
    Фикстура, возвращающая экземпляр RegisterController со всеми зависимостями,
    подменёнными на моки.
    """
    # 1. Мокаем зависимости, которые создаются внутри конструктора или методов
    mock_view = mocker.MagicMock()
    mock_api_client = mocker.MagicMock()

    # 2. Мокаем класс RegisterModel, чтобы его конструктор возвращал мок-экземпляр
    mock_model_instance = mocker.MagicMock()
    # Если нужно, можно настроить методы модели по умолчанию
    # mock_model_instance.validate.return_value = (True, {})
    mock_model_instance.register = mocker.MagicMock()

    mocker.patch(
        'ui.screen.register.register_model.RegisterModel',
        return_value=mock_model_instance
    )

    # 3. Мокаем AccessTokenManager (используется в _on_registration_success)
    mock_token_manager = mocker.MagicMock()
    mocker.patch(
        'service.token.AccessTokenManager',
        return_value=mock_token_manager
    )

    # 4. (Опционально) Мокаем rich.inspect, чтобы не было вывода в консоль
    # mocker.patch('your_package.register_controller.inspect')

    # 5. Создаём контроллер с замоканными view и api_client
    controller = RC(view=mock_view, api_client=mock_api_client)

    # 6. Сохраняем ссылки на моки, чтобы в тестах делать проверки
    # Можно вернуть только контроллер, но часто удобно вернуть всё вместе
    return {
        'controller': controller,
        'mock_view': mock_view,
        'mock_api_client': mock_api_client,
        'mock_model': mock_model_instance,
        'mock_token_manager': mock_token_manager,
    }


class TestRegisterController:
    @pytest.mark.parametrize('email, username, password', [
        ('qwe@qweq.com', 'username_1', 'password0'),
        ('qwe@qwew.com', 'username_2', 'password1'),
        ('qwe@qwee.com', 'username_3', 'password2'),])
    def test_handle_submit_positive(self, mocker, register_controller, email, username, password):
        register_controller['controller'].handle_submit(email, username, password)

        # assert register_controller['mock_model'].register.call_count == 1
