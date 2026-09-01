from ui.screen.base.model import BaseAuthModel
from schemas import RegisterFormModel


class FDRegisterModel(BaseAuthModel[RegisterFormModel]):
    endpoint = 'auth/register'
    model = RegisterFormModel
