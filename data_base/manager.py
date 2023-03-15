from typing import Union, Callable

from . import db


def check_exceptions(func: Callable[[db.Model, dict], None]) -> bool:
	def wrapper(*args, **kwargs) -> bool:
		try:
			func(*args, **kwargs)
			return True
		except:
			db.session.rollback()
			return False

	return wrapper


def commit(func) -> None:
	def wrapper(*args, **kwargs) -> None:
		value = func(*args, **kwargs)
		db.session.commit()

		return value
	return wrapper


@commit
@check_exceptions
def insert(model: db.Model, **values) -> bool:
	new_entry = model(**values)
	db.session.add(new_entry)