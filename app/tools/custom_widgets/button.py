# -*- coding: utf-8 -*-

import os

from kivy.lang import Builder
from kivymd.uix.button import MDIconButton

from config import PATTERNS_DIR


path_to_kv_file = os.path.join(PATTERNS_DIR, 'custom_widgets', 'button.kv')
Builder.load_file(path_to_kv_file)


class FDIconButton(MDIconButton):
	pass