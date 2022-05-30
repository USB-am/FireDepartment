# -*- coding: utf-8 -*-

import os

from kivy.lang import Builder
from kivymd.uix.boxlayout import MDBoxLayout

from config import PATTERNS_DIR
from app.tools.custom_widgets import FDTextField
from app.tools.custom_widgets.button import FDIconButton


path_to_kv_file = os.path.join(PATTERNS_DIR, 'fields', 'search_block.kv')
Builder.load_file(path_to_kv_file)


class SearchBlock(MDBoxLayout):
	@property
	def text_field(self) -> FDTextField:
		return self.ids.text_field

	@property
	def search_button(self) -> FDIconButton:
		return self.ids.search_button