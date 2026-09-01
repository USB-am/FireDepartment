from typing import TYPE_CHECKING, cast

from kivymd.app import MDApp
from pydantic import BaseModel

from ui.screen.base.utils import TKivyCallback


if TYPE_CHECKING:
    from .screen import BScreen
    from .model import BModel, BaseAuthModel
    from service.requests.client import APIClient
    from main import FDApplication
    from service.lang_manager import LangManager
    from utils.path_manager import PathManager


class BController[TView: BScreen | BaseAuthModel, TModel: BModel | BaseAuthModel]:
    model_type: type[TModel]

    def __init__(self, view: TView, api_client: 'APIClient'):
        self.view: TView = view
        self.model: TModel = self.model_type(api_client)

        current_app = cast('FDApplication', MDApp.get_running_app())
        self.lang_manager: 'LangManager' = current_app.lang_manager
        self.path_manager: 'PathManager' = current_app.ui.path_manager


class BaseAuthController[TView: BaseAuthModel, TModel: BaseAuthModel](BController):
    schema: type[BaseModel]

    def handle_submit(self, on_success: TKivyCallback | None=None, on_failure: TKivyCallback | None=None,
                      on_error: TKivyCallback | None=None, **fields) -> None:

        is_valid, errors = self.model.validate(**fields)
        if not is_valid and errors is not None:
            return

        self.view.show_loading(True)

        self.model.send_request(
            form_data=self.schema(**fields),
            on_success=on_success,
            on_failure=on_failure,
            on_error=on_error
        )
