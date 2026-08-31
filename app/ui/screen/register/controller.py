from typing import TYPE_CHECKING

from .model import FDRegisterModel


if TYPE_CHECKING:
    from .view import FDRegisterScreen
    from service.requests.client import APIClient


class FDRegisterController:
    def __init__(self, view: 'FDRegisterScreen', api_client: 'APIClient'):
        self.view = view
        self.model = FDRegisterModel(api_client)

    def handle_submit(self, email: str, username: str, password: str) -> None:
        is_valid, errors = self.model.validate(email, username, password)
        if errors is not None:
            for field, message in errors.items():
                self.view.show_field_error(field, message)
                return
