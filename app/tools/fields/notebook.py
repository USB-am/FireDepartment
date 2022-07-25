from os import path

from kivy.lang import Builder
from kivy.properties import StringProperty
from kivymd.uix.tab import MDTabs, MDTabsBase
from kivymd.uix.boxlayout import MDBoxLayout

from config import FIELDS_DIR, LOCALIZED
from data_base import db


path_to_kv_file = path.join(FIELDS_DIR, 'notebook.kv')
Builder.load_file(path_to_kv_file)


class Tab(MDBoxLayout, MDTabsBase):
	def __init__(self, emergency: db.Model):
		self.emergency = emergency
		self.title = emergency.title

		super().__init__()


class NoteBook(MDTabs):
	pass