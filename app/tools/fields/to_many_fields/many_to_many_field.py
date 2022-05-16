# -*- coding: utf-8 -*-

from .abstract_to_many_field import AbstractToManyField


class ManyToManyField(AbstractToManyField):
	def __init__(self, title: str):
		self.group = None
		self._table_name = title[:-1].title()

		super().__init__(title)

	def get_value(self) -> list:
		result = []

		for element in self._elements:
			if element.state:
				result.append(element.id)

		return result