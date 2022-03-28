# -*- coding: utf-8 -*-

from os.path import join as os_join

from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout

import config as Config
from UI.custom_screen import CustomScreen
from UI.custom_widgets import FDTitleLabel, FDSeparator
import db_models


path_to_kv_file = os_join(Config.PATTERNS_DIR, 'settings.kv')
Builder.load_file(path_to_kv_file)

DB_TABLES = [db_models.Tag, db_models.Rank, db_models.Position, \
	db_models.Person, db_models.Post
]


class TableSettings(BoxLayout):
	def __init__(self, table):
		self.table = table
		self.view_text = self.table.__tablename__
		self.to_create_page = f'create_{self.table.__tablename__.lower()}'
		self.to_list_edit = f'edit_{self.table.__tablename__.lower()}s'

		super().__init__()


class Settings(CustomScreen):
	name = 'settings'

	def __init__(self):
		super().__init__()

		self.__data_base_settings()

	def __data_base_settings(self) -> None:
		container = self.ids.settings_list

		for table in DB_TABLES:
			widget = TableSettings(table)
			container.add_widget(widget)