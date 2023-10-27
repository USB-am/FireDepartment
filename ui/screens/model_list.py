from typing import Union

from kivy.lang.builder import Builder
from kivy.properties import ObjectProperty
from kivymd.uix.boxlayout import MDBoxLayout

from app.path_manager import PathManager
from data_base import db
from .base_screen import BaseScreen
from config.paths import __SCREEN_MODEL_LIST


Builder.load_file(__SCREEN_MODEL_LIST)


class ListElement(MDBoxLayout):
	""" Элемент списка на странице ModelList """

	entry = ObjectProperty()


class ModelList(BaseScreen):
	""" Базовый класс отображения списка записей из БД """

	def __init__(self, *, name: str, toolbar_title: str,\
		model: db.Model, path_manager: PathManager):

		self.name = name
		self.model = model
		self.toolbar_title = toolbar_title

		super().__init__(path_manager)

		self.ids.toolbar.add_left_button(icon='menu', callback=self.open_menu)

		for entry in model.query.all():
			widget = ListElement(entry=entry)
			self.add_content(widget)
