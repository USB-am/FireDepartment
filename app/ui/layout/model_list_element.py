from typing import Callable

from kivy.lang.builder import Builder
from kivy.properties import ObjectProperty
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.expansionpanel import MDExpansionPanel, MDExpansionPanelOneLine

# from data_base import db
from config import MODEL_LIST_LAYOUTS


Builder.load_file(MODEL_LIST_LAYOUTS)


# Temp class
class db:
	Model = None


class _ModelListElementContent(MDBoxLayout):
	'''
	Содержимое выпадающей области элемента.

	~params:
	entry: db.Model - запись из БД.
	'''

	entry = ObjectProperty(defaultvalue=db.Model)


class ModelListElement(MDExpansionPanel):
	'''
	Элемента списка модели.

	entry: db.Model - запись из БД.
	'''

	def __init__(self, entry: db.Model, **options):
		self.entry = entry

		options.update({
			'content': _ModelListElementContent(entry=entry),
			'panel_cls': MDExpansionPanelOneLine(text=entry.title)
		})

		super().__init__(**options)

	def bind_edit_btn(self, callback: Callable) -> None:
		self.content.ids.edit_btn.bind(on_release=lambda *_: callback())

	def bind_info_btn(self, callback: Callable) -> None:
		self.content.ids.info_btn.bind(on_release=lambda *_: callback())
