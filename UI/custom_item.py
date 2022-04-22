# -*- coding: utf-8 -*-

import os

from kivy.lang import Builder
from kivymd.uix.boxlayout import MDBoxLayout

from settings import settings as Settings
from settings import LANG


path_to_kv_file = os.path.join(Settings.PATTERNS_DIR, 'custom_item.kv')
Builder.load_file(path_to_kv_file)

class CustomItem(MDBoxLayout):
	def __init__(self, parent_: str, text: str='', icon: str=None):
		if parent_ in ('', None) and icon is None:
			raise AttributeError(
				'Attributes "parent_" and "icon" cannot be '\
				'equial to None at the same time'
			)

		self.text = text
		if parent_ is None:
			self.icon = icon
		else:
			self.icon = Settings.ICONS.get(parent_.title(), '')

		super().__init__()