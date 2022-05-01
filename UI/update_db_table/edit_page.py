# -*- coding: utf-8 -*-

import os

from kivy.lang import Builder

from settings import settings as Settings
from db_models import Tag, Rank, Position, Person, Post
from . import AbstractPage


path_to_kv_file = os.path.join(
	Settings.PATTERNS_DIR, 'edit_page.kv')
Builder.load_file(path_to_kv_file)


class AbstractEditPage(AbstractPage):
	pass


class EditTag(AbstractEditPage):
	name = 'edit_tag'
	table = Tag


class EditRank(AbstractEditPage):
	name = 'edit_rank'
	table = Rank


class EditPosition(AbstractEditPage):
	name = 'edit_position'
	table = Position


class EditPerson(AbstractEditPage):
	name = 'edit_person'
	table = Person


class EditPost(AbstractEditPage):
	name = 'edit_post'
	table = Post