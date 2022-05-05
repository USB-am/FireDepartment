# -*- coding: utf-8 -*-

import os

from kivy.lang import Builder
from kivymd.uix.boxlayout import MDBoxLayout

from config import PATTERNS_DIR


path_to_kv_file = os.path.join(PATTERNS_DIR, 'fields', 'search_block.kv')
Builder.load_file(path_to_kv_file)


class SearchBlock(MDBoxLayout):
	pass