# -*- coding: utf-8 -*-

from sqlalchemy.orm.collections import InstrumentedList

from .abstract_to_many_field import AbstractToManyField


class ManyToManyField(AbstractToManyField):
	def __init__(self, title: str):
		self.group = None
		self._table_name = title[:-1].title()

		super().__init__(title)

	def get_value(self) -> list:
		result = InstrumentedList()

		for element in self._elements:
			if element.state:
				result.append(element._element)

		return result

	def set_value(self, active_items: list) -> None:
		for element in self._elements:
			if element._element in active_items:
				element.state = True