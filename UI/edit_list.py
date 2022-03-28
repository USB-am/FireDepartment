# -*- coding: utf-8 -*-

from os.path import join as os_join

from kivy.lang import Builder
from kivy.uix.button import Button

from config import PATTERNS_DIR
from UI.custom_screen import CustomScreen
import db_models


path_to_kv_file = os_join(PATTERNS_DIR, 'edit_list.kv')
Builder.load_file(path_to_kv_file)


class EditItem(Button):
	def __init__(self, db_row):
		self.db_row = db_row
		self.view_text = str(db_row)

		super().__init__()


class EditList(CustomScreen):
	def __init__(self):
		super().__init__()

		self.bind(on_enter=self.update_list)

	def update_list(self, instance) -> None:
		container = self.ids.edit_list
		container.clear_widgets()
		values = self.table.query.all()

		for value in values:
			widget = EditItem(value)
			container.add_widget(widget)


class EditTagList(EditList):
	name = 'edit_tags'
	table = db_models.Tag


class EditRankList(EditList):
	name = 'edit_ranks'
	table = db_models.Rank


class EditPositionList(EditList):
	name = 'edit_positions'
	table = db_models.Position


class EditPersonList(EditList):
	name = 'edit_persons'
	table = db_models.Person


class EditPostList(EditList):
	name = 'edit_posts'
	table = db_models.Post