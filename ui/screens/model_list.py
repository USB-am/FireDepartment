from typing import Union

from kivy.lang.builder import Builder
from kivy.properties import ObjectProperty
from kivymd.uix.boxlayout import MDBoxLayout

from app.path_manager import PathManager
from data_base import db, Emergency
from .base_screen import BaseScreen
from config.paths import __SCREEN_MODEL_LIST


Builder.load_file(__SCREEN_MODEL_LIST)


class ListElement(MDBoxLayout):
	""" Элемент списка на странице ModelList """

	entry = ObjectProperty()


class ModelList(BaseScreen):
	""" Базовый класс отображения списка записей из БД """

	def __init__(self, path_manager: PathManager):
		super().__init__(path_manager)

		self.ids.toolbar.add_left_button(icon='menu', callback=self.open_menu)
		self.ids.toolbar.add_right_button(
			icon='plus',
			callback=lambda *_: self.path_manager.forward(f'{self.model.__tablename__.lower()}_create')
		)

		for entry in self.model.query.all():
			widget = ListElement(entry=entry)
			widget.ids.button.bind(on_release=lambda *_: self.path_manager.forward(self.edit_link))
			self.add_content(widget)


class EmergencyList(ModelList):
	''' Список вызовов '''

	name = 'emergency_list'
	toolbar_title = 'Список выездов'
	model = Emergency
	edit_link = 'emergency_edit'
