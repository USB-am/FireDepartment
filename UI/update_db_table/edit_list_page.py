# -*- coding: utf-8 -*-

import os

from kivy.lang import Builder
from kivymd.uix.button import MDRectangleFlatIconButton

from UI.custom_screen import CustomScreen
from settings import settings as Settings
from db_models import db, Tag, Rank, Position, Person, Post


path_to_kv_file = os.path.join(
	Settings.PATTERNS_DIR, 'edit_list_page.kv')
Builder.load_file(path_to_kv_file)


class ListElement(MDRectangleFlatIconButton):
	def __init__(self, element: db.Model):
		self.element = element
		self.icon_ = Settings.ICONS.get(self.element.__tablename__, '')
		self.show_text = str(self.element)

		super().__init__()


class AbstractEditListPage(CustomScreen):
	def fill_content(self) -> None:
		self.ids.toolbar.title = self.table.__tablename__

		container = self.ids.content
		container.clear_widgets()

		elements = self.table.query.all()

		for element in elements:
			container.add_widget(ListElement(element))


class EditListTag(AbstractEditListPage):
	name = 'edit_tags'
	table = Tag


class EditListRank(AbstractEditListPage):
	name = 'edit_ranks'
	table = Rank


class EditListPosition(AbstractEditListPage):
	name = 'edit_positions'
	table = Position


class EditListPerson(AbstractEditListPage):
	name = 'edit_persons'
	table = Person


class EditListPost(AbstractEditListPage):
	name = 'edit_posts'
	table = Post