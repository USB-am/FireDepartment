# -*- coding: utf-8 -*-

from .abstract_to_many_field import AbstractToManyField


class ManyToManyField(AbstractToManyField):
	icon = 'checkbox-multiple-marked-outline'

	def __init__(self, title: str):
		self.group = None
		self._table_name = title[:-1].title()

		super().__init__(title)