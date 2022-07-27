from os import path

from kivy.lang import Builder
from kivymd.uix.expansionpanel import MDExpansionPanel, MDExpansionPanelOneLine
from kivymd.uix.boxlayout import MDBoxLayout

from data_base import db
from config import ADDITION_ELEMENTS_DIR, path_manager


path_to_kv_file = path.join(ADDITION_ELEMENTS_DIR, 'option_list_item.kv')
Builder.load_file(path_to_kv_file)


class ItemContent(MDBoxLayout):
	def __init__(self, table_name: str):
		super().__init__()

		to_create_screen = f'create_{table_name.lower()}'
		to_edit_screen = f'edit_{table_name.lower()}_list'

		self.ids.create_button.bind(on_release=lambda e: \
			path_manager.PathManager().forward(to_create_screen))
		self.ids.edit_button.bind(on_release=lambda e: \
			path_manager.PathManager().forward(to_edit_screen))


class OptionListItem(MDExpansionPanel):
	def __init__(self, table: db.Model):
		self.table = table
		self.icon = table.icon
		self.title = table.__tablename__	# TODO: rewrite

		self.content = ItemContent(self.title)
		self.panel_cls = MDExpansionPanelOneLine(text=self.title)

		super().__init__()