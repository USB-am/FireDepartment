# -*- coding: utf-8 -*-

import os

from kivy.lang import Builder

from settings import settings as Settings
from db_models import Tag, Rank, Position, Person, Post, ColorTheme
from . import AbstractPage


path_to_kv_file = os.path.join(Settings.PATTERNS_DIR, 'update_db_table.kv')
Builder.load_file(path_to_kv_file)


class CreatePage(AbstractPage):
	pass


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