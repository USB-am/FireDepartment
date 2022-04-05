# -*- coding: utf-8 -*-

from os.path import join as os_join
from datetime import datetime, timedelta

from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup

from config import PATTERNS_DIR, LANG
from .custom_screen import CustomScreen
from .custom_widgets import FDButton, FDLabel
from db_models import db as DataBase
from db_models import Person, Rank, Position
from .fields import RadioField


path_to_kv_file = os_join(PATTERNS_DIR, 'post_page.kv')
Builder.load_file(path_to_kv_file)


class TitleField(BoxLayout):
	def __init__(self, title: str):
		self.title = title

		super().__init__()


class DescriptionField(BoxLayout):
	def __init__(self, text: str):
		if text is None:
			self.text = ''
		else:
			self.text = text

		super().__init__()


class UserStateContent(BoxLayout):
	pass


class UserStatePopup(Popup):
	def __init__(self, person):
		self.person = person
		self.title = f'{self.person.name}:'
		self.content = UserStateContent()

		self.fill_content()

		super().__init__(size_hint=(.9, .9))

	def fill_content(self) -> None:
		container = self.content.ids.content

		info = {
			'Name': self.person.name,
			'Phone': self.person.phone,
			'Add_Phone': self.get_nullable_value('add_phone'),
			'Work_Day': self.get_nullable_value('work_day'),
			'Work_Type': RadioField.POINTS.get(
				self.get_nullable_value('work_type'),
				'',
			),
			'Position': self.get_person_foreignkeys_value(
				table=Position,
				id_=self.person.position
			),
			'Rank': self.get_person_foreignkeys_value(
				table=Rank,
				id_=self.person.rank
			)
		}

		for key, value in info.items():
			container.add_widget(FDLabel(
				size_hint=(1, None),
				size=(self.width, 50),
				text=f'{LANG.get(key, "-")}: {value}'
			))

	def get_nullable_value(self, column: str) -> str:
		result = getattr(self.person, column)

		if result is None:
			return ''
		return result

	def get_person_foreignkeys_value(self, table, id_: int) -> str:
		result = table.query.filter_by(id=id_).first()

		if result is None:
			return ''
		return result.title


class PersonItem(FDButton):
	def __init__(self, db_row):
		self.db_row = db_row
		self.title = db_row.name
		self.info_popup = UserStatePopup(self.db_row)

		super().__init__()

		self.bind(on_press=self.open_popup)

	def open_popup(self, instance) -> None:
		self.info_popup.open()


class TagItem(FDButton):
	def __init__(self, db_row):
		self.db_row = db_row
		self.title = db_row.title

		super().__init__()


class ListField(BoxLayout):
	def __init__(self, list_: list):
		self.list_ = sorted(list_, key=lambda item: item.id)
		self.widget_height = self.get_height()

		super().__init__()

		self.__fill_list()

	def get_height(self) -> int:
		return len(self.list_) * 60 + 30

	def __fill_list(self) -> None:
		container = self.ids.list_

		for i in self.list_:
			container.add_widget(self.ITEM(i))


class PersonListField(ListField):
	ITEM = PersonItem

	def __init__(self, persons: list):
		self.persons = persons
		self.work_persons = self.get_work_persons()

		super().__init__(self.work_persons)

		self.ids.title.text = 'Люди:'

	def __is_worked(self, person) -> bool:
		now_date = datetime.now()
		yesterday_date = now_date - timedelta(days=1)

		if person.work_type == 0 and now_date.weekday() < 5:
			return True
		elif person.work_type == 1 and person.work_day is not None:
			if self.is_relevent(person):
				return True
		elif person.work_type == 2:
			return True

		return False

	def is_relevent(self, person) -> bool:
		delta = datetime.now() - person.work_day

		return delta.days % 4 == 0

	def get_work_persons(self) -> list:
		result = [person for person in self.persons if self.__is_worked(person)]

		return result


class TagListField(ListField):
	ITEM = TagItem

	def __init__(self, tags: list):
		super().__init__(tags)

		self.ids.title.text = 'Теги:'


class PostPage(CustomScreen):
	name = 'post_page'

	def fill_info(self, db_row):
		self.ids.title_label.text = db_row.title.title()

		info_container = self.ids.info_container
		info_container.clear_widgets()

		info_container.add_widget(TitleField(db_row.title))
		info_container.add_widget(DescriptionField(db_row.description))
		info_container.add_widget(PersonListField(db_row.persons))
		info_container.add_widget(TagListField(db_row.tags))