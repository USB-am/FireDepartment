# -*- coding: utf-8 -*-

import os

from kivy.lang import Builder
from kivy.uix.togglebutton import ToggleButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRectangleFlatIconButton, MDRaisedButton
from kivymd.uix.dialog import MDDialog

import db_models
from settings import settings as Settings
from settings import LANG


path_to_kv_file = os.path.join(Settings.PATTERNS_DIR, 'fields', 'foreign_key_field.kv')
Builder.load_file(path_to_kv_file)


class ManyTo_Item(MDBoxLayout):
	def __init__(self, item_info: db_models.db.Model, group: str=None):
		self.item_info = item_info
		self.group = group

		super().__init__()

	def is_active(self) -> bool:
		return False


class TableContent(MDBoxLayout):
	def __init__(self, item_info: db_models.Person):
		self.item_info = item_info

		super().__init__()


class ManyTo_PersonItem(MDBoxLayout):
	def __init__(self, item_info: db_models.db.Model, group: str=None):
		# self.item_info = item_info
		self.item_info = db_models.Person.query.first()
		self.group = group

		super().__init__()

		self.ids.show_info.bind(on_press=self.open_dialog)

	def open_dialog(self, instance) -> None:
		MDDialog(
			type="custom",
			content_cls=TableContent(self.item_info),
			buttons=[
				MDRaisedButton(
					text='OK',
					on_press=lambda e: e.parent.parent.parent.parent.dismiss()
				)
			]
		).open()

	def is_active(self) -> bool:
		return False


class ForeignKeyField(MDBoxLayout):
	def __init__(self, title: str):
		title = title.title()

		self.group_name = title
		self.icon = Settings.ICONS.get(title, '')
		self.table = getattr(db_models, title)
		self.title = LANG.get(title, title)

		super().__init__()

		self.rows = []

		self.fill_container()

	def fill_container(self) -> None:
		container = self.ids.container
		container.clear_widgets()

		items = self.table.query.all()

		for item in items:
			widget = ManyTo_PersonItem(
				item_info=item,
				group=self.group_name
			)

			container.add_widget(widget)
			self.rows.append(widget)

	def get_value(self) -> db_models.db.Model:
		for row in self.rows:
			if row.is_active():
				return row.item_info