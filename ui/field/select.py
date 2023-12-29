from typing import Callable, List, Union

from kivy.lang.builder import Builder
from kivymd.uix.boxlayout import MDBoxLayout

from data_base import db
from config import SELECT_FIELD
from ui.layout.select import FDSelectListElement


Builder.load_file(SELECT_FIELD)


class _BaseSelect(MDBoxLayout):
	'''
	Поле выбора нескольких элементов из модели БД.

	~params:
	title: str - текст над списком;
	dialog_content: MDBoxLayout - содержимое окна с информацией;
	model: db.Model - модель БД, элементы которой будут отображены;
	group: str=None - группа объектов. Если None, доступен выбор множества элементов.
	'''

	def __init__(self, title: str, dialog_content: MDBoxLayout, model: db.Model, group: str):
		self.title = title
		self.dialog_content = dialog_content
		self.model = model
		self.group = group

		super().__init__()

		self.elements: List[FDSelectListElement] = []
		self.fill_elements()

	def fill_elements(self) -> None:
		''' Заполняет список элементами из модели '''

		entries = self.model.query.order_by(self.model.title)
		for entry in entries:
			list_elem = FDSelectListElement(
				entry=entry,
				info_content=self.dialog_content,
				group=self.group)
			self.elements.append(list_elem)
			self.ids.content.add_widget(list_elem)

	def bind_btn(self, callback: Callable) -> None:
		''' Привязать событие нажатия кнопки на верхней панели '''

		self.ids.add_btn.bind(on_release=lambda *_: callback())

	def bind_checkbox(self, callback: Callable) -> None:
		''' Привязать событие нажатия чекбокса '''

		for element in self.elements:
			element.ids.checkbox.bind(on_release=lambda e: callback())


class FDSelect(_BaseSelect):
	'''
	Поле выбора одного элемента из модели БД.

	~params:
	title: str - текст над списком;
	dialog_content: MDBoxLayout - содержимое окна с информацией;
	model: db.Model - модель БД, элементы которой будут отображены;
	group: str - группа объектов. Если None, доступен выбор множества элементов.
	'''

	def get_value(self) -> Union[int, None]:
		for element in self.elements:
			if element.ids.checkbox.active:
				return element.entry.id

		return None

	def set_value(self, entry: db.Model) -> None:
		for element in self.elements:
			if element.entry.id == entry:
				element.ids.checkbox.active = True
			else:
				element.ids.checkbox.active = False


class FDMultiSelect(_BaseSelect):
	'''
	Поле выбора нескольких элементов из модели БД.

	~params:
	title: str - текст над списком;
	dialog_content: MDBoxLayout - содержимое окна с информацией;
	model: db.Model - модель БД, элементы которой будут отображены.
	'''

	def __init__(self, **kwargs):
		kwargs.update({'group': None})

		super().__init__(**kwargs)

	def get_value(self) -> List[db.Model]:
		output = [element.entry for element in self.elements \
			if element.ids.checkbox.active]

		return output

	def set_value(self, entries: List[db.Model]) -> None:
		for element in self.elements:
			if element.entry in entries:
				element.ids.checkbox.active = True
			else:
				element.ids.checkbox.active = False
