# -*- coding: utf-8 -*-

import os

from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from flask_sqlalchemy import sqlalchemy
from sqlalchemy.sql.sqltypes import String, Integer, DateTime, Time

import config as Config
from db_models import db, Tag, Rank, Position, Person, Post
from UI.calendar_field import Calendar

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


class EditRanks(EditPages):
	name = 'edit_ranks'
	table = Rank


class EditPositions(EditPages):
	name = 'edit_positions'
	table = Position


class EditPersons(EditPages):
	name = 'edit_persons'
	table = Person




class StringField(BoxLayout):
	def __init__(self, show_text: str, value: str):
		self.show_text = show_text
		if value is None:
			self.value = ''
		else:
			self.value = value

		super().__init__()

	def get_value(self):
		return self.ids.text_input.text


class EditPage(Screen):
	def __init__(self):
		super().__init__()

		self.ids.apply_changes_button.bind(on_press=self.apply_changes)

	def apply_changes(self, instance) -> None:
		values = self.get_fields_values()
		print(values)
		db.session.query(self.table).filter_by(id=self.item.id).update(values)
		db.session.commit()

	def get_fields_values(self) -> dict:
		result = {}

		for children in self.ids.fields_frame.children:
			result[children.show_text.lower()] = children.get_value()

		return result

	def get_item(self, item) -> None:
		self.item = item
		self.__create_fields()

	def __create_fields(self) -> None:
		self.update_title()
		self.show_fields()

	def update_title(self) -> None:
		self.ids.title.text = str(self.item)

	def show_fields(self) -> None:
		container = self.ids.fields_frame
		container.clear_widgets()
		columns_info = self.__get_columns_info()

		for column in columns_info:
			if isinstance(column['type'], String):
				widget = self.create_string_field(column)
				container.add_widget(widget)

			elif isinstance(column['type'], DateTime):
				widget = self.create_calendar_field(column)
				container.add_widget(widget)

			elif isinstance(column['type'], Time):
				# print(f'{column} is Time field!')
				pass

			elif isinstance(column['type'], Integer):
				# print(f'{column} is Integer field!')
				pass

	def create_string_field(self, column) -> StringField:
		return StringField(
			show_text=column['name'].title(),
			value=getattr(self.item, column['name'])
		)

	def create_calendar_field(self, column: dict) -> Calendar:
		return Calendar(
			show_text=column['name'].title(),
			now_set_date=self.item.work_day
		)

	def __get_columns_info(self) -> list:
		columns = self.item.__table__.columns.keys()[1:]
		columns_obj = [getattr(self.table, column) for column in columns]
		columns_info = db.session.query(*columns_obj).column_descriptions

		return columns_info


class EditTag(EditPage):
	name = 'edit_tag'
	table = Tag


class EditRank(EditPage):
	name = 'edit_rank'
	table = Rank


class EditPosition(EditPage):
	name = 'edit_position'
	table = Position


class EditPerson(EditPage):
	name = 'edit_person'
	table = Person