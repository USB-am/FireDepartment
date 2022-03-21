# -*- coding: utf-8 -*-

import os

from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout

import config as Config
from db_models import Tag, Rank, Position, Person, Post

__all__ = ('EditTags', 'EditTag', )


Builder.load_file(os.path.join(Config.PATTERNS_DIR, 'edit_page.kv'))


class EditDBRow(BoxLayout):
	def __init__(self, db_item, to_page):
		self.db_item = db_item
		self.to_page = to_page

		super().__init__()


class EditPages(Screen):
	def __init__(self):
		super().__init__()

		self.bind(on_enter=self.show_all_db_rows)

	def show_all_db_rows(self, instance) -> None:
		container = self.ids.db_row_frame
		container.clear_widgets()
		items = self.table.query.all()

		for item in items:
			container.add_widget(EditDBRow(item, self.name[:-1]))


class EditTags(EditPages):
	name = 'edit_tags'
	table = Tag


class EditPage(Screen):
	def __init__(self):
		super().__init__()

	def get_item(self, item) -> None:
		self.item = item
		self.__create_fields()

	def __create_fields(self) -> None:
		self.update_title()
		self.show_fields()

	def update_title(self) -> None:
		self.ids.title.text = str(self.item.title)

	def show_fields(self) -> None:
		print(dir(self.item))
		print(dir(self.item.query))
		print(self.item.query.column_descriptions)


class EditTag(EditPage):
	name = 'edit_tag'