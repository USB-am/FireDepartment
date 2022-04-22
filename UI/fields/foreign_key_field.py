# -*- coding: utf-8 -*-

import os

from kivy.lang import Builder
from kivy.uix.togglebutton import ToggleButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.dialog import MDDialog

# from UI.custom_item import CustomItem
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

		self.fill_content()

	def fill_content(self) -> None:
		container = self.ids.table_content_container
		container.clear_widgets()

		fields = getattr(db_models, self.item_info.__tablename__).get_fields()

		for field in fields.keys():
			title_field = field.title()
			icon = Settings.ICONS.get(title_field, '')
			title = LANG.get(title_field, '')
			value = getattr(self.item_info, field)
			text = f'{title}: {value}'
			container.add_widget(MDLabel(
				text=text
			))
			#container.add_widget(CustomItem(
			#	parent_=field,
			#	text=text
			#))


class ManyTo_PersonItem(MDBoxLayout):
	dialog = None

	def __init__(self, item_info: db_models.db.Model, group: str=None):
		# self.item_info = item_info
		self.item_info = db_models.Person.query.first()
		self.group = group

		super().__init__()

		self.ids.show_info.bind(on_press=self.open_dialog)

	def open_dialog(self, instance) -> None:
		if self.dialog is None:
			self.dialog = MDDialog(
				title=f'{self.item_info.name}',
				type='custom',
				content_cls=TableContent(self.item_info)
			)

		self.dialog.open()

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
		container = self.ids.foreign_key_container
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