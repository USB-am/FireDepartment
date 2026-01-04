from typing import Any, Optional

from . import (
    ValidationResult,
    _BaseValidator,
    _check_unique_column,
    _check_excluding_unique_column,
    _check_not_empty,
    _check_not_zero)
from data_base.model import db


class ModelValidator(_BaseValidator):
    ''' Базовый валидатор для создания моделей '''
    def __init__(self, model: db.Model, column: str):
        self.model = model
        self.column = column


class UniqueValidator(_BaseValidator):
    ''' Валидация на уникальность '''

    def __call__(self, value: Any, text: str='Поле должно быть уникальным') -> ValidationResult:
        check = _check_unique_column(self.model, self.column, value)
        return ValidationResult(text, check)


class UniqueExcludingValidator(_BaseValidator):
    ''' Валидация на уникальность, за исключением 1 записи '''

    def __init__(self, model: db.Model, column: str, entry: db.Model):
        super().__init__(model, column)
        self.entry = entry

    def __call__(self,
                 value: Any,
                 text: Optional[str]='Поле должно быть уникальным'
                 ) -> ValidationResult:
        check = _check_excluding_unique_column(
            model=self.model,
            column=self.column,
            value=value,
            entry=self.entry)
        return ValidationResult(text, check)


class EmptyValidator(_BaseValidator):
    ''' Валидация на пустое значение '''

    def __call__(self, value: Any,
                 text: Optional[str]='Поле не может быть пустым') -> ValidationResult:
        check = _check_not_empty(value)
        return ValidationResult(text, check)


class ZeroValidator(_BaseValidator):
    ''' Валидация на значение >0 '''

    def __call__(self, value: int,
                 text: Optional[str]='Значение должно быть больше 0') -> ValidationResult:
        if not value or not value.isdigit():
            return ValidationResult(text, False)
        check = _check_not_zero(int(value))
        return ValidationResult(text, check)
