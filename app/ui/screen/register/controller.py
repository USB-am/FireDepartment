from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from .view import FDRegisterScreen


class FDRegisterController:
    def __init__(self, view: 'FDRegisterScreen'):
        self.view = view

    def handle_submit(self, email: str, username: str, password: str) -> None:
        print(f'{email=}\n{username=}\n{password=}')
