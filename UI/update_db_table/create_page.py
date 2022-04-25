# -*- coding: utf-8 -*-

import os

from kivy.lang import Builder
from kivymd.uix.button import MDRectangleFlatButton

from settings import settings as Settings
from db_models import Tag, Rank, Position, Person, Post, ColorTheme
from . import AbstractPage


path_to_kv_file = os.path.join(Settings.PATTERNS_DIR, 'update_db_table.kv')
Builder.load_file(path_to_kv_file)


class CreatePage(AbstractPage):
	def submit(self, instance: MDRectangleFlatButton) -> None:
		for widget in self.widgets:
			try:
				value = widget.get_value()
				print(f'{widget.title} has value {value}')
			except AttributeError:
				print(f'{widget.title} has not method .get_value')


class CreateTag(CreatePage):
	table = Tag
	name = 'create_tag'


class CreateRank(CreatePage):
	table = Rank
	name = 'create_rank'


class CreatePosition(CreatePage):
	table = Position
	name = 'create_position'


class CreatePerson(CreatePage):
	table = Person
	name = 'create_person'


class CreatePost(CreatePage):
	table = Post
	name = 'create_post'


class CreateColorTheme(CreatePage):
	table = ColorTheme
	name = 'create_color_theme'