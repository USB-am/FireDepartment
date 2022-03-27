# -*- coding: utf-8 -*-

from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout

import config as Config


# ============== #
# === Labels === #
class FDLabel(Label):
	def __init__(self, **options):
		options.update({
			'color': Config.FONT_COLOR,
			'font_size': Config.FONT_SIZE
		})
		super().__init__(**options)


class FDTitleLabel(Label):
	def __init__(self, **options):
		options.update({
			'color': Config.FONT_COLOR,
			'font_size': Config.FONT_TITLE_SIZE
		})
		super().__init__(**options)
# === Labels === #
# ============== #


# =============== #
# === Buttons === #
class FDButton(Button):
	def __init__(self, image_path=None, **options):
		options.update({
			'background_color': Config.BUTTON_COLOR,
			'color': Config.FONT_COLOR
		})
		super().__init__(**options)
# === Buttons === #
# =============== #


# ================= #
# === Separator === #
class FDSeparator(BoxLayout):
	def __init__(self, **options):
		options.update({
			'size_hint': (1, None),
			'size': (self.width, 10),
			'padding': (0, 4, 0, 4)
		})
		super().__init__(**options)
# === Separator === #
# ================= #