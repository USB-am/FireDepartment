# -*- coding: utf-8 -*-

import os

from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics.context_instructions import Color

import config as Config
from db_models import Tag, Rank, Position, Person, Post
from .custom_widgets import CustomScreen


Builder.load_file(os.path.join(Config.PATTERNS_DIR, 'settings.kv'))


TABLES = (
	(Tag,      'create_tags',      'edit_tags'     ),
	(Rank,     'create_ranks',     'edit_ranks'    ),
	(Position, 'create_positions', 'edit_positions'),
	(Person,   'create_persons',   'edit_persons'  ),
	(Post,     'create_posts',     'edit_posts'    ),
)


class EditRow(BoxLayout):
	def __init__(self, table, to_create: str, to_edit: str):
		self.table = table
		self.to_create = to_create
		self.to_edit = to_edit

		super().__init__()


class Settings(CustomScreen):
	name = 'settings'

	def __init__(self):
		super().__init__()

		self.__show_db_operations()

	def __show_db_operations(self) -> None:
		container = self.ids.settings_frame

		for table, to_create, to_edit in TABLES:
			container.add_widget(EditRow(table, to_create, to_edit))