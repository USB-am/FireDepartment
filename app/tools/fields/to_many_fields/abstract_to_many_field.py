# -*- coding: utf-8 -*-

import os

from kivy.lang import Builder
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.dialog import MDDialog
from kivymd.uix.label import MDLabel

from config import PATTERNS_DIR, LOCALIZED
import data_base


path_to_kv_file = os.path.join(PATTERNS_DIR, 'fields', 'to_many_fields',
	'abstract_to_many_field.kv')
Builder.load_file(path_to_kv_file)


class DialogContent(MDBoxLayout):
	def __init__(self, element: data_base.db):
		self._element = element
		super().__init__()

		self.__init_ui()

	def __init_ui(self) -> None:
		for title in self._element.get_fields().keys():
			key = MDLabel(
				text=f'{LOCALIZED.translate(title)}:',
				halign='left',
				size_hint=(.4, None),
				size=(self.width, 50))
			value = MDLabel(
				text=f'{getattr(self._element, title)}',
				size_hint=(.6, None),
				size=(self.width, 50))
			self.add_widget(key)
			self.add_widget(value)


class ElementToManyField(MDBoxLayout):
	def __init__(self, element: data_base.db, group: str=None):
		self._element = element
		self.display_text = self._element.title
		self.group = group

		super().__init__()

		self.dialog = MDDialog(
			title=self.display_text,
			type='custom',
			content_cls=DialogContent(self._element),
			size_hint=(.9, .8)
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