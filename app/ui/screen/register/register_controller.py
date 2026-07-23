import os
from typing import Optional

from .register_model import RegisterModel
# from service.token import AccessTokenManager
from service.user_data import UserData
from service.current_user import CurrentUser


class RegisterController:
    def __init__(self, view: 'FDRegisterScreen', api_client: 'APIClient'):
        self.view = view
        self.api_client = api_client

        self.model = RegisterModel(self.api_client)
        self.view.set_controller(self)

    def handle_submit(self, email: str, username: str, password: str) -> None:
        is_valid, errors = self.model.validate(email, username, password)
        if not is_valid:
            for field, msg in errors.items():
                self.view.show_field_error(field, msg)
            return

        self.view.show_loading(True)

        self.model.register(
            email=email,
            username=username,
            password=username,
            on_success=self._on_registration_success,
            on_failure=self._on_registration_failure,
            on_redirect=self._on_registration_redirect,
            on_cancel=self._on_registration_cancel,
            on_error=self._on_registration_error
        )

    def _on_registration_success(self, response, message: Optional[str]=None) -> None:
        self.view.show_loading(False)

        # from rich import inspect
        # inspect(response, all=True)

        base_dir = os.getcwd()
        new_user = CurrentUser(base_dir, base_dir)

        result = response.result

        new_user.save_user_data(UserData(
            id=result['id'],
            email=result['email'],
            username=result['username']))
        new_user.save_token(
            result['access_token'],
            result['refresh_token'])

        self.api_client.set_token(result['access_token'])

        self.view.path_manager.move_to_screen('options')

    def _on_registration_failure(self, response, message: str) -> None:
        self.view.show_loading(False)
        self.view.open_dialog(title='Failure', message=message['detail'])

    def _on_registration_redirect(self, response, message: str) -> None:
        self.view.show_loading(False)
        self.view.open_dialog(title='Redirect', message=str(message))

    def _on_registration_cancel(self, response, message: str) -> None:
        self.view.show_loading(False)
        self.view.open_dialog(title='Cancel', message=str(message))

    def _on_registration_error(self, response, message: str) -> None:
        self.view.show_loading(False)
        self.view.open_dialog(title='Error', message=str(message))
