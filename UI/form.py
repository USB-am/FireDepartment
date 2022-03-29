# -*- coding: utf-8 -*-

from os.path import join as os_join

from kivy.lang import Builder

from config import PATTERNS_DIR
from .custom_screen import CustomScreen
from .custom_widgets import FDButton
from . import fields
from db_models import Tag, Rank, Position, Person, Post


path_to_kv_file = os_join(PATTERNS_DIR, 'form.kv')
Builder.load_file(path_to_kv_file)


class Form(CustomScreen):
	def update_screen(self, table_id: int=None) -> None:
		container = self.ids.field_list
		container.clear_widgets()

		for title, field_name in self.table.get_fields().items():
			field = getattr(fields, field_name)(
				title=title
			)

			if table_id is not None:
				db_row = self.table.query.filter_by(id=table_id).first()
				field.set_value(getattr(db_row, title))

			container.add_widget(field)

	def get_value(self) -> dict:
		childrens = self.ids.field_list.children

		for children in childrens:
			print(children.title, children.get_value(), sep=' - ')

class CreateForm(Form):
	def update_screen(self) -> None:
		super().update_screen()

		create_btn = self.ids.bottom_button
		create_btn.text = 'Создать'
		create_btn.bind(on_press=self.insert_values)

	def insert_values(self, instance) -> None:
		print('Create button is pressed!')
		self.get_value()


class EditForm(Form):
	def update_screen(self, table_id: int) -> None:
		super().update_screen(table_id)

		edit_btn = self.ids.bottom_button
		edit_btn.text = 'Изменить'
		edit_btn.bind(on_press=self.update_values)

	def update_values(self, instance) -> None:
		print('Edit button is pressed!')
		self.get_value()


# ==================== #
# === Create forms === #
class CreateTag(CreateForm):
	name = 'create_tag'
	table = Tag


class CreateRank(CreateForm):
	name = 'create_rank'
	table = Rank


class CreatePosition(CreateForm):
	name = 'create_position'
	table = Position


class CreatePerson(CreateForm):
	name = 'create_person'
	table = Person


class CreatePost(CreateForm):
	name = 'create_post'
	table = Post
# === Create forms === #
# ==================== #


# ================== #
# === Edit forms === #
class EditTag(EditForm):
	name = 'edit_tag'
	table = Tag


class EditRank(EditForm):
	name = 'edit_rank'
	table = Rank


class EditPosition(EditForm):
	name = 'edit_position'
	table = Position


class EditPerson(EditForm):
	name = 'edit_person'
	table = Person


class EditPost(EditForm):
	name = 'edit_post'
	table = Post
# === Edit forms === #
# ================== #