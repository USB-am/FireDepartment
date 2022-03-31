# -*- coding: utf-8 -*-

from os.path import join as os_join

from kivy.lang import Builder

from config import PATTERNS_DIR
from .custom_screen import CustomScreen
from .custom_widgets import FDButton
from . import fields
from . import exceptions
from db_models import db as DataBase
from db_models import Tag, Rank, Position, Person, Post


path_to_kv_file = os_join(PATTERNS_DIR, 'form.kv')
Builder.load_file(path_to_kv_file)


class Form(CustomScreen):
	TABLE_ID = None
	NEXT_PAGE = 'settings'

	def update_screen(self) -> None:
		container = self.ids.field_list
		container.clear_widgets()

		for title, field_name in self.table.get_fields().items():
			field = getattr(fields, field_name)(
				title=title
			)

			if self.TABLE_ID is not None:
				db_row = self.table.query.filter_by(id=self.TABLE_ID).first()
				field.set_value(getattr(db_row, title))

			container.add_widget(field)

	def get_value(self) -> dict:
		childrens = self.ids.field_list.children

		result = {children.title: children.get_value() \
			for children in childrens}

		return result


class CreateForm(Form):
	def update_screen(self) -> None:
		super().update_screen()

		create_btn = self.ids.bottom_button
		create_btn.text = 'Создать'

	@exceptions.db_exception
	def insert_values(self) -> None:
		values = super().get_value()
		new_db_row = self.table(**values)

		DataBase.session.add(new_db_row)
		DataBase.session.commit()


class EditForm(Form):
	def update_screen(self) -> None:
		super().update_screen()

		edit_btn = self.ids.bottom_button
		edit_btn.text = 'Изменить'

	@exceptions.db_exception
	def insert_values(self) -> None:
		fields = self.table.get_fields()

		values = super().get_value()
		db_row = self.table.query.filter_by(id=self.TABLE_ID)

		for key, value in fields.items():
			if value == 'ManyToManyField':
				field = values.pop(key)
				self._update_posts(db_row, field)

		db_row.update(values)

		DataBase.session.commit()

	def _update_posts(self, db_row, field) -> None:
		item = db_row.first()
		item.posts = field


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