# -*- coding: utf-8 -*-

import os

from kivy.lang import Builder
from kivymd.uix.textfield import MDTextField

from config import PATTERNS_DIR


path_to_kv_file = os.path.join(PATTERNS_DIR, 'custom_widgets', 'text_field.kv')
Builder.load_file(path_to_kv_file)


class FDTextField(MDTextField):
	pass