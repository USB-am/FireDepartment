from typing import TYPE_CHECKING, cast

from kivymd.app import MDApp


if TYPE_CHECKING:
    from .screen import BScreen
    from .model import BModel
    from service.requests.client import APIClient
    from main import FDApplication
    from service.lang_manager import LangManager



class BController:
    model_type: type[BModel]

    def __init__(self, view: 'BScreen', api_client: 'APIClient'):
        self.view = view
        self.model = self.model_type(api_client)

        current_app = cast('FDApplication', MDApp.get_running_app())
        self.lang_manager: 'LangManager' = current_app.lang_manager
