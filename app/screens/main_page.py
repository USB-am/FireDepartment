# -*- coding: utf-8 -*-

import os

from kivy.lang import Builder
from app.tools.custom_widgets import CustomScreen

from config import PATTERNS_DIR


path_to_kv_file = os.path.join(PATTERNS_DIR, 'screens', 'main_page.kv')
Builder.load_file(path_to_kv_file)


class MainPage(CustomScreen):
	name = 'main_page'