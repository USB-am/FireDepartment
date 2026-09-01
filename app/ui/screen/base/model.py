from typing import TYPE_CHECKING

from pydantic import BaseModel, ValidationError

from ui.screen.base.utils import TKivyCallback


if TYPE_CHECKING:
    from service.requests.client import APIClient


class BModel:
    def __init__(self, api_client: 'APIClient'):
        self.api_client = api_client


class BaseAuthModel[TValidationModel: BaseModel](BModel):
    schema: type[TValidationModel]
    endpoint: str

    def validate(self, **fields) -> tuple[bool, dict[str, str] | None]:
        try:
            self.schema(**fields)
            return True, None

        except ValidationError as validation_errors:
            errors: dict[str, str] = {}

            for err in validation_errors.errors():
                field = str(err['loc'][0])
                errors[field] = err['msg']
            return False, errors

    def send_request(self, form_data: TValidationModel, on_success: TKivyCallback,
                     on_failure: TKivyCallback, on_cancel: TKivyCallback | None = None,
                     on_error: TKivyCallback | None = None
    ) -> None:

        self.api_client.post(
            endpoint=self.endpoint,
            data=form_data.model_dump(),
            on_success=on_success,
            on_failure=on_failure,
            on_cancel=on_cancel,
            on_error=on_error
        )
