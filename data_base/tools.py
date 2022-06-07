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
	db.session.add(new_empty)
	db.session.commit()


@check_db_commit_except
def update_row(element: db.Model, values: dict) -> None:
	for column_name, value in values.items():
		setattr(element, column_name, value)

	db.session.commit()


@check_db_commit_except
def delete_row(element: db.Model) -> None:
	db.session.delete(element)

	db.session.commit()


@check_db_commit_except
def create_base_theme() -> None:
	theme_element = ColorTheme.query.first()

	if theme_element is None:
		theme = ColorTheme(
			primary_palette='BlueGray',
			accent_palette='Teal',
			primary_hue='900',
			theme_style='Light'
		)

		db.session.add(theme)
		db.session.commit()