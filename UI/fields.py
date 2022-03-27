# -*- coding: utf-8 -*-

from os.path import join as os_join

from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout

from config import PATTERNS_DIR


path_to_kv_file = os_join(PATTERNS_DIR, 'fields.kv')
Builder.load_file(path_to_kv_file)


class StringField(BoxLayout):
	def __init__(self, db_row):
		self.db_row = db_row
		self.view_text = str(self.db_row)

		super().__init__()