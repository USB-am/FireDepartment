from typing import Any
from dataclasses import dataclass

# from data_base.model import db


@dataclass
class ValidationResult:
    text: str
    status: bool

    def __str__(self):
        return self.text


class _BaseValidator:
    pass


def _check_unique_column(model: 'db.Model', column: str, value: Any) -> bool:
    '''
    Проверка value на уникальность в колонке.

    ~params:
    model: db.Model - модель в которой будет идти поиск;
    column: str - название колонки;
    value: Any - значение, с которым необходимо сравнить.
    '''

    entries = model.query.filter(getattr(model, column)==value).all()

    return not bool(entries)


def _check_excluding_unique_column(model: 'db.Model', column: str, value: Any,
                                   entry: 'db.Model') -> bool:
    '''
    Проверка уникальности нового значения entry.

    ~params:
    model: db.Model - модель в которой будет идти поиск;
    column: str - название колонки;
    value: Any - значение, с которым необходимо сравнить;
    entry: db.Model - запись, которая будет проигнорированна при поиске.
    '''

    entries = model.query.filter(getattr(model, column)==value).all()
    return (entry in entries) or (not entries)


def _check_not_empty(value: Any) -> bool:
    '''
    Проверка value на не пустое значение.

    ~params:
    value: Any - значение для проверки.
    '''

    return bool(value)


def _check_not_zero(value: int) -> bool:
    '''
    Проверка value > 0

    ~params:
    value: int - целое значение для проверки.
    '''

    return value > 0