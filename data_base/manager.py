from . import db
from uix.dialog import FDDialog, ExceptionDialogContent
from config import LOCALIZED

from kivymd.uix.button import MDRaisedButton


def Dialog(error: Exception):
	ok_button = MDRaisedButton(text=LOCALIZED.translate('Ok'))
	dialog = FDDialog(
		title=LOCALIZED.translate('Error!'),
		content=ExceptionDialogContent(
			'Возникла ошибка!\n\n'
			'Возможные причины:\n'
			'1. Одно из обязательных полей не заполнено;\n'
			'2. В поле, которое должно быть уникальным, введены '
			'неуникальные данные\n'
			'3. Просто произошла какая-то хрень :D\n\n'
			f'{error}'),
		buttons=[ok_button,]
	)
	ok_button.bind(on_release=lambda e: dialog.dismiss())

	return dialog


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