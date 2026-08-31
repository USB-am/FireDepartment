from typing import TYPE_CHECKING, Callable, Any

from pydantic import BaseModel, EmailStr, ValidationError


if TYPE_CHECKING:
    from service.requests.client import APIClient
    from kivy.network.urlrequest import UrlRequest


TKivyCallback = Callable[['UrlRequest', Any], None]


class AuthFormModel(BaseModel):
    email: EmailStr
    password: str


class FDAuthModel:
    def __init__(self, api_client: 'APIClient'):
        self.api_client = api_client

    def validate(self, email: EmailStr, password: str) -> tuple[bool, dict[str, str] | None]:
        try:
            AuthFormModel(email=email,
                          password=password)
            return True, None

        except ValidationError as validation_errors:
            errors: dict[str, str] = {}

            for err in validation_errors.errors():
                field = str(err['loc'][0])
                errors[field] = err['msg']
            return False, errors

    def send_register_request(self, email: EmailStr, password: str,
                            on_success: TKivyCallback, on_failure: TKivyCallback,
                            on_cancel: TKivyCallback | None=None, on_error: TKivyCallback | None=None
    ) -> None:
        try:
            data = AuthFormModel(email=email, password=password)
        except ValidationError as error:
            on_failure(None, str(error))
            return

        self.api_client.post(
            endpoint='auth/login',
            data=data.model_dump(),
            on_success=on_success,
            on_failure=on_failure,
            on_cancel=on_cancel,
            on_error=on_error
        )
