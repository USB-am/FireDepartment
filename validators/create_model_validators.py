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


@staticmethod
def tag_create_validate(params: Dict[str, Widget]) -> Union[bool, Widget]:
	''' Валидатор для формы создания Tag '''

	checks = [
		_check_unique_column(Tag, 'title', params['title'].get_value()),
		_check_not_empty(params['title'].get_value()),
	]

	return all(checks)


def rank_create_validate(params: Dict[str, Widget]) -> None:
	''' Валидатор для формы создания Rank '''

	checks = [
		_check_unique_column(Rank, 'title', params['title'].get_value()),
		_check_not_empty(params['title'].get_value()),
		_check_not_empty(params['priority'].get_value()),
	]

	return all(checks)


def position_create_validate(params: Dict[str, Widget]) -> None:
	''' Валидатор для формы создания Position '''

	checks = [
		_check_unique_column(Position, 'title', params['title'].get_value()),
		_check_not_empty(params['title'].get_value()),
	]

	return all(checks)


def human_create_validate(params: Dict[str, Widget]) -> None:
	''' Валидатор для формы создания Human '''

	checks = [
		_check_not_empty(params['title'].get_value()),
	]

	return all(checks)


def emergency_create_validate(params: Dict[str, Widget]) -> None:
	''' Валидатор для формы создания Emergency '''

	checks = [
		_check_unique_column(Emergency, 'title', params['title'].get_value()),
	]

	return all(checks)


def worktype_create_validate(params: Dict[str, Widget]) -> None:
	''' Валидатор для формы создания Worktype '''

	checks = [
		_check_unique_column(Worktype, 'title', params['title'].get_value()),
		_check_not_empty(params['title'].get_value()),
		_check_not_empty(params['start_work_day'].get_value()),
		_check_not_empty(params['finish_work_day'].get_value()),
		_check_not_empty(params['work_day_range'].get_value()),
		_check_not_empty(params['week_day_range'].get_value()),
	]

	return all(checks)


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

	def __call__(self, value: Any) -> ValidationResult:
		check = _check_unique_column(self.model, self.column, value)
		return ValidationResult('Поле должно быть уникальным', check)


class EmptyValidator(_BaseValidator):
	''' Валидация на пустое значение '''

	def __call__(self, value: Any) -> ValidationResult:
		check = _check_not_empty(value)
		return ValidationResult('Поле не может быть пустым', check)
