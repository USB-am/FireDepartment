from typing import Any, Iterable, Generator

from sqlalchemy import or_

from data_base import db


class Paginator(list):
	''' Пагинатор '''

	def __init__(self, *elements: db.Model):
		super().__init__(*elements)
		self.__all_elements = elements

	def paginate_by(self, elements: Iterable[Any]=None, count: int=10) -> Generator:
		''' Получить генератор, возвращающий по count ВСЕХ элементов '''

		if elements is None:
			elements = self.__all_elements.copy()

		while elements:
			yield elements.pop(0)

	def filter_by(self, *fields: str, value: str, count: int=10) -> Generator:
		''' Получить генератор, возвращающий по count сортированных элементов '''

		if len(self):
			return iter(())

		model = self[0].__class__
		filtered_entries = model.query.filter(
			or_(
				*[getattr(model, field).like(f'%{value}%') \
				for field in fields]
			)
		)

		return self.paginate_by(filtered_entries)


class ElementController:
	'''
	Контроллер для управления пагинацией.

	~params:
	*elements: db.Model - записи БД.
	'''

	def __init__(self, *elements: db.Model):
		self.elements = elements
		self.paginator = Paginator(*elements)

	def paginate(self, count: int=10) -> Generator:
		'''
		Получить генератор элементов для пагинации.

		~params:
		count: int=10 - количество элементов, возвращенные одной итерацией.
		'''

		return self.paginator.paginate_by(count)

	def find_elements(self, *fields: str, text: str, count: int=10) -> Generator:
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
		self.paginator = Paginator(*self.paginator)

		return self.paginate(count)
