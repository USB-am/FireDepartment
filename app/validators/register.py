from typing import Optional

from . import (
    ValidationResult,
    _BaseValidator)
from ui.field.input import _BaseInput


class FieldEqualsField(_BaseValidator):
    ''' Значение поля1 == Значение поля2 '''

    def __call__(self,
                 field_1: _BaseInput,
                 field_2: _BaseInput,
                 text: str) -> ValidationResult:
        status = field_1.get_value() == field_2.get_value()
        return ValidationResult(text, status)
