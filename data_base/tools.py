# -*- coding: utf-8 -*-

from . import db, ColorTheme
from app.exceptions.custom_exceptions import DataBaseUpdateError


def check_db_commit_except(func):
	def wrapper(*args, **kwargs):
		try:
			return func(*args, **kwargs)
		except Exception as error:
			db.session.rollback()

			raise DataBaseUpdateError(error)

	return wrapper


@check_db_commit_except
def create_empty(table: db.Model, values: dict) -> None:
	new_empty = table(**values)


@check_db_commit_except
def create_base_theme() -> None:
	theme_element = ColorTheme.query.first()

	if theme_element is None:
		theme = ColorTheme(
			theme='BlueGray',
			accent='Teal',
			hue='200',
			style='Light'
		)

		db.session.add(theme)
		db.session.commit()