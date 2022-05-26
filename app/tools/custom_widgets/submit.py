# -*- coding: utf-8 -*-

import os

from kivy.lang import Builder
from kivy.uix.button import Button

from config import PATTERNS_DIR, LOCALIZED


path_to_kv_file = os.path.join(PATTERNS_DIR, 'custom_widgets', 'submit.kv')
Builder.load_file(path_to_kv_file)


class Submit(Button):
	def __init__(self, **kw):
		super().__init__(**kw)