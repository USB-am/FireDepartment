# -*- coding: utf-8 -*-

from .abstract_to_many_field import AbstractToManyField
from data_base import db


class ForeignKeyField(AbstractToManyField):
	def __init__(self, title: str):
		self.group = title
		self._table_name = title.title()

		super().__init__(title)

	def get_value(self) -> db.Model:
		for element in self._elements:
			if element.state:
				return element._element