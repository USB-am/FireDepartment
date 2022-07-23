from os import path

from kivy.lang import Builder
from kivymd.uix.boxlayout import MDBoxLayout

from config import ADDITION_ELEMENTS_DIR
from data_base import db


path_to_kv_file = path.join(ADDITION_ELEMENTS_DIR, 'main_page_list_element.kv')
Builder.load_file(path_to_kv_file)


class MainPageListElement(MDBoxLayout):
	def __init__(self, db_row: db.Model):
		self.db_row = db_row

		super().__init__()