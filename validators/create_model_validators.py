from typing import Any, Optional
from dataclasses import dataclass

from data_base.model import db


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


def _check_excluding_unique_column(model: db.Model, column: str, value: Any,
	                                 entry: db.Model) -> bool:
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
