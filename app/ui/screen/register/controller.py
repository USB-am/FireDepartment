import uuid
from typing import TYPE_CHECKING, Any

from pydantic import EmailStr

from schemas import RegisterFormModel
from ui.screen.base.controller import BaseAuthController
from ui.screen.register.model import FDRegisterModel
from service.requests.storage import UserProfile, TokenData


if TYPE_CHECKING:
    from kivy.network.urlrequest import UrlRequestUrllib


class FDRegisterController(BaseAuthController):
    model_type = FDRegisterModel
    schema = RegisterFormModel

    def handle_submit(self, email: EmailStr, username: str, password: str) -> None:
        super().handle_submit(
            email=email,
            username=username,
            password=password,
            on_success=self._on_success,
            on_failure=self._on_failure,
            on_error=self._on_error
        )

    def _on_success(self, response: 'UrlRequestUrllib', message: dict[str, Any]) -> None:
        self.view.show_loading(False)
        self.view.open_dialog(self.lang_manager.get_text('complete'), str(message))

        self.store.save_profile(UserProfile(id=uuid.UUID(message['id']),
                                            email=message['email'],
                                            username=message['username']))
        self.store.save_token(TokenData(access_token=message['access_token'],
                                        refresh_token=message['refresh_token']))

        self.path_manager.move_to_screen('options')

    def _on_failure(self, response: 'UrlRequestUrllib', message: dict[str, Any]) -> None:
        print(f'this _on_failure method')
        self.view.show_loading(False)
        self.view.open_dialog(
            title=self.lang_manager.get_text('failure'),
            message=message.get('detail', 'Произошла ошибка!'))

    def _on_error(self, response: 'UrlRequestUrllib', message: dict[str, Any]) -> None:
        print(f'this _on_error method')
        self.view.show_loading(False)
        self.view.open_dialog(self.lang_manager.get_text('error'), str(message))
