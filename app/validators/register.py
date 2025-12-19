import re

from . import (
    ValidationResult,
    _BaseValidator)
from ui.field.input import _BaseInput


def _is_valid_email(email: str) -> bool:
    regex = r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w+$'
    return bool(re.match(regex, email))


class CorrectedEmailValidator(_BaseValidator):
    ''' Email корректен '''
    def __init__(self,
                 email_field: _BaseInput,
                 message: str):
        super().__init__()
        self.email_field = email_field
        self.message = message

    def __call__(self, _: str) -> ValidationResult:
        if (field_text := self.email_field.get_value()) is None:
            field_text = ''
        status = _is_valid_email(field_text)
        return ValidationResult(self.message, status)


class EmptyFieldValidator(_BaseValidator):
    ''' Проверка на пустое поле '''

    def __init__(self, field: _BaseInput, message: str):
        super().__init__()
        self.field = field
        self.message = message

    def __call__(self, _: str) -> ValidationResult:
        return ValidationResult(self.message, bool(self.field.get_value()))


class FieldEqualsFieldValidator(_BaseValidator):
    ''' Значение поля1 == Значение поля2 '''

    def __init__(self,
                 field_1: _BaseInput,
                 field_2: _BaseInput,
                 message: str):
        super().__init__()
        self.field_1 = field_1
        self.field_2 = field_2
        self.message = message

    def __call__(self, _: str) -> ValidationResult:
        status = self.field_1.get_value() == self.field_2.get_value()
        return ValidationResult(self.message, status)
