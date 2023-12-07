from kivy.lang.builder import Builder
from kivymd.uix.boxlayout import MDBoxLayout

from data_base import db
from config import SELECT_FIELD
from ui.layout.select import FDSelectListElement
from ui.layout.dialogs import EmergencyDialogContent


Builder.load_file(SELECT_FIELD)


class FDMultiSelect(MDBoxLayout):
	'''
	Поле выбора нескольких элементов из модели БД.

	~params:
	title: str - текст над списком;
	model: db.Model - модель БД, элементы которой будут отображены.
	'''

	def __init__(self, title: str, model: db.Model):
		self.title = title
		self.model = model

		super().__init__()

		self.fill_elements()

	def fill_elements(self) -> None:
		''' Заполняет список элементами из модели '''

		entries = self.model.query.order_by(self.model.title)
		for entry in entries:
			list_elem = FDSelectListElement(entry=entry, info_content=EmergencyDialogContent)
			self.ids.content.add_widget(list_elem)
