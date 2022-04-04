# -*- coding: utf-8 -*-

from os.path import join as os_join

from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout

from config import PATTERNS_DIR
from .custom_screen import CustomScreen


path_to_kv_file = os_join(PATTERNS_DIR, 'post_page.kv')
Builder.load_file(path_to_kv_file)


class DescriptionField(BoxLayout):
	def __init__(self, text: str):
		if text is None:
			self.text = ''
		else:
			self.text = text

		super().__init__()


class PostPage(CustomScreen):
	name = 'post_page'

	def fill_info(self, db_row):
		self.ids.title_label.text = db_row.title.title()

		info_container = self.ids.info_container
		info_container.clear_widgets()

		info_container.add_widget(DescriptionField(db_row.description))