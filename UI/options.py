# -*- coding: utf-8 -*-

import os

from kivy.lang import Builder
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.expansionpanel import MDExpansionPanel, MDExpansionPanelOneLine

from settings import settings as Settings
from .custom_screen import CustomScreen
from db_models import Tag, Rank, Position, Person, Post, ColorTheme


path_to_kv_file = os.path.join(Settings.PATTERNS_DIR, 'options.kv')
Builder.load_file(path_to_kv_file)


TABLES = (
	(Tag, 'Теги', Settings.ICONS['Tag']),
	(Rank, 'Звания', Settings.ICONS['Rank']),
	(Position, 'Должности', Settings.ICONS['Position']),
	(Person, 'Люди', Settings.ICONS['Person']),
	(Post, 'ЧС', Settings.ICONS['Post']),
	(ColorTheme, 'Внешний вид', Settings.ICONS['ColorTheme'])
)


class TableItem(MDBoxLayout):
	def __init__(self, table):
		self.table = table
		self.to_create = f'create_{self.table.__tablename__}'.lower()
		self.to_edit = f'edit_{self.table.__tablename__}s'.lower()

		super().__init__()


class Options(CustomScreen):
	name = 'options'

	def __init__(self):
		super().__init__()

		self.update_screen()

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