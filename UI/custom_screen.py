# -*- coding: utf-8 -*-

import os

from kivy.lang import Builder
from kivy.uix.screenmanager import Screen

from settings import settings as Settings


path_to_kv_file = os.path.join(Settings.PATTERNS_DIR, 'custom_screen.kv')
Builder.load_file(path_to_kv_file)


class CustomScreen(Screen):
	pass