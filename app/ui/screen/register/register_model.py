from typing import Tuple, Dict, Callable, Optional

from kivymd.app import MDApp
from pydantic import BaseModel, EmailStr, ValidationError


class RegisterData(BaseModel):
    email: EmailStr
    username: str
    password: str


class RegisterModel:
    def __init__(self, api_client: 'APIClient'):
        self.api_client = api_client

    def validate(self, email: str, username: str, password: str) -> Tuple[bool, Optional[Dict]]:
        try:
            data = RegisterData(
                email=email,
                username=username,
                password=password)

            return True, None

        except ValidationError as error:
            errors = {}

            for err in e.errors():
                field = err['loc'][0]
                errors[field] = err['msg']

            return False, errors

    def register(self, email: str, username: str, password: str,
                 on_success: Callable, on_failure: Callable,
                 on_redirect: Callable, on_cancel: Callable,
                 on_error: Callable) -> None:
        try:
            data = RegisterData(
                email=email,
                username=username,
                password=password)

        except ValidationError as error:
            on_failure(None, str(error))
            return

        self.api_client.post(
            endpoint='users/register',
            data=data.model_dump(),
            on_success=on_success,
            on_failure=on_failure,
            on_redirect=on_redirect,
            on_cancel=on_cancel,
            on_error=on_error
        )
