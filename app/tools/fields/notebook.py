from os import path

from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivymd.uix.tab import MDTabs, MDTabsBase
from kivymd.uix.boxlayout import MDBoxLayout

from config import FIELDS_DIR, LOCALIZED
from data_base import db, Emergency
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

		self.scrolled_layout.add_widgets(SelectedList('Humans'))

		self.scrolled_layout.add_widgets(*[FDLabel(f'Row {i+1}', f'Text #{i+1}') \
			for i in range(100)])


class NoteBook(MDTabs):
	pass