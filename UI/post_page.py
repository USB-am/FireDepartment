# -*- coding: utf-8 -*-

from os.path import join as os_join

from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout

from config import PATTERNS_DIR, LANG
from .custom_screen import CustomScreen
from .custom_widgets import FDButton, FDLabel


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


class UserStatePopup(Popup):
	def __init__(self, person):
		self.person = person
		self.title = f'{self.person.name}:'
		self.content = UserStateContent()

		super().__init__(size_hint=(.9, .9))


class PersonItem(FDButton):
	def __init__(self, db_row):
		self.db_row = db_row
		self.title = db_row.name

		super().__init__()

		self.bind(on_press=self.open_popup)

	def open_popup(self, instance) -> None:
		print('open_popup')


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
		return len(self.list_) * 60 + 20

	def __fill_list(self) -> None:
		container = self.ids.list_

		for i in self.list_:
			container.add_widget(self.ITEM(i))


class PersonListField(ListField):
	ITEM = PersonItem

	def __init__(self, persons: list):
		super().__init__(persons)

		self.ids.title.text = 'Люди:'


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