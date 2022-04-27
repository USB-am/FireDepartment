# -*- coding: utf-8 -*-

import os

from kivy.lang import Builder
from kivymd.uix.label import MDLabel, MDIcon

from settings import settings as Settings


path_to_kv_file = os.path.join(
	Settings.PATTERNS_DIR, 'widgets', 'label.kv')
Builder.load_file(path_to_kv_file)


class AbstractLabel(MDLabel):
	font_color = (0, 0, 0, 1)
	font_size = 16


class AbstractIcon(MDIcon):
	font_color = (0, 0, 0, 1)
	font_size = 16


class FDLabel(AbstractLabel):
	font_color = Settings.FONT_COLOR
	font_size = Settings.FONT_SIZE


class FDInvertedLabel(AbstractLabel):
	font_color = Settings.INVERTED_FONT_COLOR
	font_size = Settings.FONT_SIZE


class MDIcon(AbstractIcon):
	font_color = Settings.FONT_COLOR
	font_size = Settings.FONT_SIZE


class FDInvertedIcon(MDIcon):
	font_color = Settings.INVERTED_FONT_COLOR
	font_size = Settings.FONT_SIZE