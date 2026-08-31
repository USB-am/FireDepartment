from typing import TYPE_CHECKING

from pydantic import BaseModel, EmailStr, ValidationError


if TYPE_CHECKING:
    from service.requests.client import APIClient


class RegisterFormModel(BaseModel):
    email: EmailStr
    username: str
    password: str


class FDRegisterModel:
    def __init__(self, api_client: 'APIClient'):
        self.api_client = api_client

    def validate(self, email: str, username: str, password: str) -> tuple[bool, dict[str, str] | None]:
        try:
            RegisterFormModel(email=email,
                              username=username,
                              password=password)
            return True, None

        except ValidationError as validation_errors:
            errors: dict[str, str] = {}

            for err in validation_errors.errors():
                field = str(err['loc'][0])
                errors[field] = err['msg']
            return False, errors
