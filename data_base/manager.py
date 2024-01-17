from typing import Any, Dict, Type, Union
from sqlalchemy.orm import exc

from data_base import db
from exceptions.data_base import DBCommitError, DBAddError


def add(func):
	def wrapper(*args, **kwargs):
		try:
			entry = func(*args, **kwargs)
			db.session.add(entry)

			return entry

		except exc.sa_exc.SQLAlchemyError as error:
			raise DBAddError

	return wrapper


def commit(func):
	def wrapper(*args, **kwargs):
		try:
			output = func(*args, **kwargs)
			db.session.commit()

			return output

		except exc.sa_exc.SQLAlchemyError as error:
			raise DBCommitError

	return wrapper


@commit
@add
def write_entry(model: Type[db.Model], params: Dict[str, Any]) -> db.Model:
	'''
	Создать запись в БД.

	~params:
	model: Type[db.Model] - модель, в которую будет произведена запись;
	params: Dict[str, Any] - словарь с данными о записи.
	'''

	entry = model(**params)
	return entry


@commit
def update_entry(entry: Union[db.Model, None], params: Dict[str, Any]) -> None:
	'''
	Обновить данные записи.

	~params:
	entry: Union[db.Model, None] - запись для обновления;
	params: Dict[str, Any] - параметры для обновления.
	'''

	if entry is None:
		return

	for column, value in params.items():
		setattr(entry, column, value)
