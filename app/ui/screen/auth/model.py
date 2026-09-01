from ui.screen.base.model import BaseAuthModel
from schemas import AuthFormModel


class FDAuthModel(BaseAuthModel[AuthFormModel]):
    endpoint = 'auth/login'
    schema = AuthFormModel
