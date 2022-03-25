# -*- coding: utf-8 -*-

import os

from kivy.lang import Builder
from kivy.uix.screenmanager import Screen

import config as Config


Builder.load_file(os.path.join(Config.PATTERNS_DIR, 'custom_widgets.kv'))


class CustomScreen(Screen):
	def __init__(self):
		super().__init__()