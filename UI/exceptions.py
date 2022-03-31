# -*- coding: utf-8 -*-

from flask_sqlalchemy import sqlalchemy

from db_models import db as DataBase
from UI.custom_widgets import FDErrorMessage


def global_exception(func):
	def wrapper(*args, **kwargs):
		#try:
		result = func(*args, **kwargs)

		return result

		#except Exception as error:
		#	print(error)
		#	FDErrorMessage(f'Неизвестная ошибка!\n\n{str(error)}').open()

	return wrapper


def db_exception(func):
	def wrapper(*args, **kwargs):
		try:
			result = func(*args, **kwargs)

			return result

		except sqlalchemy.exc.IntegrityError as error_message:
			error_text = 'Поле не может быть пустым!\n\n'\
				f'{error_message.orig}'

			DataBase.session.rollback()
			FDErrorMessage(error_text).open()

	return wrapper