from typing import Any, Dict, Union
from dataclasses import dataclass

from kivy.uix.widget import Widget

from data_base import db, Tag, Rank, Position, Human, Emergency, Worktype


def _check_unique_column(model: db.Model, column: str, value: Any) -> bool:
	'''
	Проверка value на уникальность в колонке.

	~params:
	model: db.Model - модель в которой будет идти поиск;
	column: str - название колонки;
	value: Any - значение, с которым необходимо сравнить.
	'''

	entries = model.query.filter(getattr(model, column)==value).all()

	return not bool(entries)


def _check_not_empty(value: Any) -> bool:
	'''
	Проверка value на не пустое значение.

	~params:
	value: Any - значение для проверки.
	'''

	return bool(value)


@dataclass
class ValidationResult:
	text: str
	status: bool

	def __str__(self):
		return self.text


class _BaseValidator:
	def __init__(self, model: db.Model, column: str):
		self.model = model
		self.column = column


class UniqueValidator(_BaseValidator):
	''' Валидация на уникальность '''

	def __call__(self, value: Any, text: str='Поле должно быть уникальным') -> ValidationResult:
		check = _check_unique_column(self.model, self.column, value)
		return ValidationResult(text, check)


class EmptyValidator(_BaseValidator):
	''' Валидация на пустое значение '''

	def __call__(self, value: Any,
	             text: str='Поле не может быть пустым') -> ValidationResult:
		check = _check_not_empty(value)
		return ValidationResult(text, check)
