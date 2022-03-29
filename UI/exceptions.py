# -*- coding: utf-8 -*-

from flask_sqlalchemy import sqlalchemy

from UI.custom_widgets import FDErrorMessage


def global_exception(func):
	def wrapper(*args, **kwargs):
		try:
			result = func(*args, **kwargs)

			return result

		except Exception as error:
			print(dir(error))

			FDErrorMessage(str(error)).open()

	return wrapper


def db_exception(func):
	def wrapper(*args, **kwargs):
		try:
			result = func(*args, **kwargs)

			return result

		except sqlalchemy.exc.IntegrityError as error_message:
			error_text = f'{error_message.orig}\n\n'\
				'Поле не может быть пустым!'

			FDErrorMessage(error_text).open()

	return wrapper