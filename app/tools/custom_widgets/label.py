# -*- coding: utf-8 -*-

import os

from kivy.lang import Builder
from kivymd.uix.label import MDIcon, MDLabel

from config import PATTERNS_DIR


path_to_kv_file = os.path.join(PATTERNS_DIR, 'custom_widgets', 'label.kv')
Builder.load_file(path_to_kv_file)


class FDLabel(MDLabel):
	pass


class FDIcon(MDIcon):
	pass