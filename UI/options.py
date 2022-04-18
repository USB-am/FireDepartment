# -*- coding: utf-8 -*-

import os

from kivy.lang import Builder
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.expansionpanel import MDExpansionPanel, MDExpansionPanelOneLine

from settings import settings as Settings
from .custom_screen import CustomScreen
from db_models import Tag, Rank, Position, Person, Post


path_to_kv_file = os.path.join(Settings.PATTERNS_DIR, 'options.kv')
Builder.load_file(path_to_kv_file)


TABLES = (
	(Tag, 'Теги', 'pound'),
	(Rank, 'Звания', 'chevron-triple-up'),
	(Position, 'Должности', 'crosshairs-gps'),
	(Person, 'Люди', 'account-group'),
	(Post, 'Ранги пожаров', 'fire-alert')
)


class TableItem(MDBoxLayout):
	def __init__(self, table):
		super().__init__()


class Options(CustomScreen):
	name = 'options'

	def __init__(self):
		super().__init__()

		self.update_screen()

	def move_to_back(self) -> None:
		self.manager.current = Settings.PATH_MANAGER.back()

	def update_screen(self) -> None:
		container = self.ids.container
		container.clear_widgets()

		for table, title, icon in TABLES:
			container.add_widget(MDExpansionPanel(
				icon=icon,
				content=TableItem(table),
				panel_cls=MDExpansionPanelOneLine(
					text=title
				)
			))