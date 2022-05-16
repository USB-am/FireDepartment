# -*- coding: utf-8 -*-

import os

from kivy.lang import Builder

from app.tools.custom_widgets import FDTextField
from config import PATTERNS_DIR, LOCALIZED


path_to_kv_file = os.path.join(PATTERNS_DIR, 'fields', 'description_field.kv')
Builder.load_file(path_to_kv_file)


class DescriptionField(FDTextField):
	icon = 'text-box-edit'

	def __init__(self, title: str):
		self.title = title
		self.display_text = self.title.title()

		super().__init__()