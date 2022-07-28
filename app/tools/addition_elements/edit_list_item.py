from os import path

from kivy.lang import Builder
from kivymd.uix.boxlayout import MDBoxLayout

from data_base import db
from config import ADDITION_ELEMENTS_DIR, path_manager


path_to_kv_file = path.join(ADDITION_ELEMENTS_DIR, 'edit_list_item.kv')
Builder.load_file(path_to_kv_file)


class EditListItem(MDBoxLayout):
	def __init__(self, db_row: db.Model):
		self.db_row = db_row

		super().__init__()

		self.ids.button.bind(on_release=lambda e: self.open_edit_page())

	def open_edit_page(self) -> None:
		edit_page_name = f'edit_{self.db_row.__tablename__.lower()}'
		edit_page = path_manager.PathManager().forward(edit_page_name)
		edit_page._update_content(self.db_row)