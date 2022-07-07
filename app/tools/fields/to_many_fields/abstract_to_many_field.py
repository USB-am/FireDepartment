# -*- coding: utf-8 -*-

import os

from kivy.lang import Builder
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.dialog import MDDialog

from config import PATTERNS_DIR, LOCALIZED
import data_base


path_to_kv_file = os.path.join(PATTERNS_DIR, 'fields', 'to_many_fields',
	'abstract_to_many_field.kv')
Builder.load_file(path_to_kv_file)


class DialogElement(MDBoxLayout):
	def __init__(self, title, value):
		self.title = title
		self.value = value

		super().__init__()


class DialogContent(MDBoxLayout):
	def __init__(self, element: data_base.db):
		super().__init__()

		self.__element = element
		self.update_content()

	def __get_values(self) -> dict:
		rows = self.__element.get_fields().keys()
		return {key: getattr(self.__element, key) for key in rows}

	def update_content(self) -> None:
		self.clear_widgets()

		for title, value in self.__get_values().items():
			print(title, value)
			self.add_widget(DialogElement(title, value))


class ElementToManyField(MDBoxLayout):
	def __init__(self, element: data_base.db, group: str=None):
		self._element = element
		self.display_text = self._element.title
		self.group = group

		super().__init__()

		self.dialog = MDDialog(
			title=self.display_text,
			type='custom',
			content_cls=DialogContent(self._element)
		)

	@property
	def state(self) -> bool:
		return self.ids.checkbox.active

	@state.setter
	def state(self, status: bool) -> None:
		self.ids.checkbox.active = status

	@property
	def id(self) -> int:
		return self._element.id

	def show_display_info(self) -> None:
		self.dialog.open()


class AbstractToManyField(MDBoxLayout):
	def __init__(self, title: str):
		self.title = title
		self.display_text = LOCALIZED.translate(self.title)
		self._table = getattr(data_base, self._table_name)
		self.icon = self._table.icon
		self.to_create_screen = f'create_{self._table_name.lower()}'

		super().__init__()

		self._elements = []
		self.update_content()

	def update_content(self) -> None:
		elements = data_base.db.session.query(self._table)\
			.order_by(self._table.title).all()

		if not elements:
			return

		container = self.ids.content
		container.clear_widgets()

		for element in elements:
			el = ElementToManyField(
				element=element,
				group=self.group
			)
			self._elements.append(el)
			container.add_widget(el)

	def clear(self) -> None:
		for element in self._elements:
			element.state = False