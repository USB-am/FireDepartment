from kivy.lang.builder import Builder
from kivy.properties import StringProperty
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel

from config import paths
from data_base import db


Builder.load_file(paths.SELECTED_LIST_FIELD)


class _SelectListItem(MDBoxLayout):
	''' Элемент списка FDSelectList '''

	def __init__(self, db_entry: db.Model):
		self.db_entry = db_entry

		super().__init__()


class FDSelectList(MDBoxLayout):
	''' Список с checkbox'ами '''

	icon = StringProperty()
	title = StringProperty()
	group = StringProperty(None)

	def add(self, row_data: db.Model) -> None:
		element = _SelectListItem(row_data)
		self.ids.lst.add_widget(element)