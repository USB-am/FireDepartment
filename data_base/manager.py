from . import db

from exceptions import Dialog


def check_insert_exception(func):
	def wrapper(*args, **kwargs):
		try:
			return func(*args, **kwargs)
		except Exception as error:
			db.session.rollback()
			Dialog(error).open()
			return False

	return wrapper


def save_changes(func):
	def wrapper(*args, **kwargs):
		entry = func(*args, **kwargs)

		db.session.commit()
		return True

	return wrapper


@check_insert_exception
@save_changes
def insert(model: db.Model, values: dict) -> None:
	entry = model(**values)
	db.session.add(entry)

	return entry


@check_insert_exception
@save_changes
def update(entry: db.Model, values: dict) -> None:
	for attr, value in values.items():
		setattr(entry, attr, value)

	return entry


@check_insert_exception
@save_changes
def delete(entry: db.Model) -> None:
	db.session.delete(entry)