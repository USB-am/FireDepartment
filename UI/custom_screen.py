# -*- coding: utf-8 -*-

from os.path import join as os_join

from kivy.lang import Builder
from kivy.uix.screenmanager import Screen

from config import PATTERNS_DIR


path_to_kv_file = os_join(PATTERNS_DIR, 'custom_screen.kv')
Builder.load_file(path_to_kv_file)


class CustomScreen(Screen):
	pass