from typing import TYPE_CHECKING, cast

from kivymd.app import MDApp
from pydantic import EmailStr

from .model import FDAuthModel
from schemas import AuthFormModel


if TYPE_CHECKING:
    from .view import FDAuthScreen
    from main import FDApplication
    from service.lang_manager import LangManager
    from service.requests.client import APIClient


class FDAuthController:
    def __init__(self, view: 'FDAuthScreen', api_client: 'APIClient'):
        self.view = view
        self.model = FDAuthModel(api_client)

        current_app = cast('FDApplication', MDApp.get_running_app())
        self.lang_manager: 'LangManager' = current_app.lang_manager

    def handle_submit(self, email: EmailStr, password: str) -> None:
        is_valid, errors = self.model.validate(email=email, password=password)
        if not is_valid and errors is not None:
            return

        self.view.show_loading(True)

        self.model.send_request(
            form_data=AuthFormModel(
                email=email,
                password=password
            ),
            on_success=self._on_success,
            on_failure=self._on_failure,
            on_error=self._on_error
        )

    def _on_success(self, response, message: str) -> None:
        print(f'this _on_success method\n{message=}')
        self.view.show_loading(False)
        self.view.open_dialog(self.lang_manager.get_text('complete'), str(message))

    def _on_failure(self, response, message: dict[str, str]) -> None:
        print(f'this _on_failure method')
        self.view.show_loading(False)
        self.view.open_dialog(
            title=self.lang_manager.get_text('failure'),
            message=message.get('detail', 'Произошла ошибка!'))

    def _on_error(self, response, message: str) -> None:
        print(f'this _on_error method')
        self.view.show_loading(False)
        self.view.open_dialog(self.lang_manager.get_text('error'), str(message))
