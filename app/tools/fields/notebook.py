from os import path

from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivymd.uix.tab import MDTabs, MDTabsBase
from kivymd.uix.boxlayout import MDBoxLayout

from config import FIELDS_DIR, LOCALIZED
from data_base import db, Emergency, Human, Tag
from app.tools.fields.label import FDLabel
from app.tools.fields.selected_list import SelectedList
from app.tools.scroll_layout import FDScrollLayout


path_to_kv_file = path.join(FIELDS_DIR, 'notebook.kv')
Builder.load_file(path_to_kv_file)


class Tab(MDBoxLayout, MDTabsBase):
	def __init__(self, db_row: db.Model):
		self.db_row = db_row
		self.title = db_row.title
		self.icon = db_row.icon

		super().__init__()


class TabEmergency(Tab):
	def __init__(self, emergency: Emergency):
		super().__init__(emergency)

		self.scrolled_layout = FDScrollLayout()
		self.add_widget(self.scrolled_layout)

		humans_icon = Human.icon
		humans_list = SelectedList(humans_icon, 'Humans')
		humans_list.update_content(self.db_row.humans)
		self.scrolled_layout.add_widgets(humans_list)

		tag_icon = Tag.icon
		tag_list = SelectedList(tag_icon, 'Tags')
		tag_list.update_content(self.db_row.tags)
		self.scrolled_layout.add_widgets(tag_list)


class NoteBook(MDTabs):
	pass