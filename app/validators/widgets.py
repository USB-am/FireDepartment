from typing import TYPE_CHECKING

from email_validator import validate_email, EmailNotValidError

from . import BaseValidator, ValidatorResult


if TYPE_CHECKING:
    from ui.widgets.text_field import _BaseTextField


class EmptyValidator(BaseValidator):
    def __call__(self, value: str, message: str | None=None) -> ValidatorResult:
        status = bool(value)

        return ValidatorResult(
            status=status,
            message=message if message is not None else self.error_msg)


class EmailValidator(BaseValidator):
    def __call__(self, value: str, message: str | None=None) -> ValidatorResult:
        try:
            validate_email(value, check_deliverability=False)
            status = True
        except EmailNotValidError:
            status = False

        return ValidatorResult(
            status=status,
            message=message if message is not None else self.error_msg)


class IdenticalPasswords(BaseValidator):
    def __init__(self, other_widget: '_BaseTextField', *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.other_widget = other_widget

    def __call__(self, value: str, message: str | None=None) -> ValidatorResult:
        status = value == self.other_widget.get_value()

        return ValidatorResult(
            status=status,
            message=message if message is not None else self.error_msg)
