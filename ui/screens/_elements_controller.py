from time import time
from typing import Type, Generator, Callable

from data_base import db
from ui.widgets.search import FDSearch


class Paginator(list):
	''' Пагинатор '''

	def __init__(self, *args):
		self._elements = args

		super().__init__(*args)

	def paginate_by(self, count: int) -> Generator:
		''' Получить функцию-генератор, возвращающий count элементов '''

		while self._elements:
			yield self._elements[:count]
			self._elements = self._elements[count:]


class ElementController:
	'''
	Контроллер для управления пагинацией.

	~params:
	model: Type[db.Model] - таблица БД из которой будут браться данные для элеметов;
	paginator: Paginator - экземпляр Пагинатора.
	'''

	def __init__(self, model: Type[db.Model], paginator: Paginator):
		self.model = model
		self.paginator = paginator

		self.current_paginator = iter(())

	def get_paginator(self, count: int=10) -> Generator:
		'''
		Получить генератор элементов для пагинации.

		~params:
		count: int=10 - количество элементов, возвращенные одной итерацией.
		'''

		self.current_paginator = self.paginator.paginate_by(count)
		return self.current_paginator

	def find_elements(self, text: str, count: int=10) -> Generator:
		'''
		Получить генератор элементов для пагинации после поиска.

		~params:
		text: str - текст по которому будет идти поиск в БД;
		count: int=10 - количество элементов, возвращенные одной итерацией.
		'''

		filtered_entries = self.model.query\
			.filter(self.model.title.like(f'%{text}%'))\
			.order_by(self.model.title)\
			.all()
		filtered_entries = [i for i in range(100)]
		self.paginator = Paginator(*self.paginator)

		return self.get_paginator()
