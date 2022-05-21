# -*- coding: utf-8 -*-

from . import db
from app.exceptions.custom_exceptions import DataBaseUpdateError


def create_empty(table: db.Model, values: dict) -> None:
	try:
		new_empty = table(**values)

		db.session.add(new_empty)
		db.session.commit()

	except Exception as error:
		db.session.rollback()

		raise DataBaseUpdateError(error)