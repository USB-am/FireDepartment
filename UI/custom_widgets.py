# -*- coding: utf-8 -*-

from os.path import join as os_join

from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup

import config as Config


path_to_kv_file = os_join(Config.PATTERNS_DIR, 'custom_widgets.kv')
Builder.load_file(path_to_kv_file)


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


# ===================== #
# === Error message === #
class FDErrorMessage(Popup):
	title = 'Ошибка!'

	def __init__(self, error_message: str):
		self.content = _FDErrorContent(error_message)

		super().__init__(size_hint=(.7, .7))


class _FDErrorContent(BoxLayout):
	def __init__(self, error_message: str):
		self.error_message = error_message

		super().__init__()
# === Error message === #
# ===================== #