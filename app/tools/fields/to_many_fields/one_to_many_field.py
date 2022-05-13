# -*- coding: utf-8 -*-

from .abstract_to_many_field import AbstractToManyField


class ForeignKeyField(AbstractToManyField):
	def __init__(self, title: str):
		self.group = title
		self._table_name = title.title()

		super().__init__(title)