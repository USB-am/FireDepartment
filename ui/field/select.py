from typing import Callable

from kivy.lang.builder import Builder
from kivymd.uix.boxlayout import MDBoxLayout

from data_base import db
from config import SELECT_FIELD
from ui.layout.select import FDSelectListElement


Builder.load_file(SELECT_FIELD)


class FDMultiSelect(MDBoxLayout):
	'''
	Поле выбора нескольких элементов из модели БД.

	~params:
	title: str - текст над списком;
	model: db.Model - модель БД, элементы которой будут отображены.
	'''

	def __init__(self, title: str, dialog_content: MDBoxLayout, model: db.Model, group: str=None):
		self.title = title
		self.dialog_content = dialog_content
		self.model = model
		self.group = group

		super().__init__()

		self.fill_elements()

	def fill_elements(self) -> None:
		''' Заполняет список элементами из модели '''

		entries = self.model.query.order_by(self.model.title)
		for entry in entries:
			list_elem = FDSelectListElement(
				entry=entry,
				info_content=self.dialog_content,
				group=self.group)
			self.ids.content.add_widget(list_elem)

	def bind_btn(self, callback: Callable) -> None:
		''' Привязать событие нажатия кнопки на верхней панели '''

		self.ids.add_btn.bind(on_release=lambda *_: callback())
