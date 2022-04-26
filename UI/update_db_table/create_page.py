# -*- coding: utf-8 -*-

import os

from kivy.lang import Builder
from kivymd.uix.button import MDRectangleFlatButton, MDRaisedButton
from kivymd.uix.dialog import MDDialog

from settings import settings as Settings
from db_models import db as DataBase
from db_models import Tag, Rank, Position, Person, Post, ColorTheme
from . import AbstractPage


path_to_kv_file = os.path.join(Settings.PATTERNS_DIR, 'update_db_table.kv')
Builder.load_file(path_to_kv_file)


class FinishedInfo(MDDialog):
	def __init__(self, text: str):
		self.text = text
		self.buttons = [MDRaisedButton(text='OK'),]
		super().__init__()


class SuccessInfo(FinishedInfo):
	def __init__(self):
		super().__init__(text='Успешно!')


class ErrorInfo(FinishedInfo):
	def __init__(self, error_message: str):
		super().__init__(error_message)


def check_db_exceptions(method):
	def wrapper(*args, **kwargs):
		try:
			method_result = method(*args, **kwargs)
			SuccessInfo().open()
			return method_result
		except Exception as error:
			# print(f'Dir error:\n{dir(error)}')
			ErrorInfo(str(error)).open()

	return wrapper


class DataBaseSaveManager:
	@staticmethod
	@check_db_exceptions
	def insert(table: DataBase.Model, values: dict) -> None:
		print(f'DataBaseSaveManager get values:\n{values}')
		new_item = table(**values)
		DataBase.session.add(new_item)
		DataBase.session.commit()


class CreatePage(AbstractPage):
	def submit(self, instance: MDRectangleFlatButton) -> None:
		values = self.get_field_values()
		print(values)
		DataBaseSaveManager.insert(self.table, values)

	def get_field_values(self) -> dict:
		return {widget.column_name: widget.get_value() for widget in self.widgets}


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