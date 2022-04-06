# -*- coding: utf-8 -*-

from os.path import join as os_join

from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.colorpicker import ColorPicker

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


# ======================== #
# === Phone text input === #
class FDPhoneTextInput(TextInput):
	MASK = '+7 (495) ___-__-__'
	_PATTERN = r'\+?[78](\d{3})(\d{3})(\d{2})(\d{2})'
	_REPL = r'+7 (\1) \2-\3-\4'
	#re.sub(
	#	pattern,
	#	r'+7 (\1) \2-\3-\4',
	#	'88005553535'
	#)

	def __init__(self, **options):
		super().__init__(**options)

		self.text = self.MASK
		self.wrapper_number = '7495'
		# self.insert_filter = 'int'

	#def on_focus(self, instance, is_focus) -> None:
	#	if is_focus:
	#		instance.cursor = (4, 0)

	def insert_text(self, substring: str, from_undo: bool=False) -> None:
		true_conditions = (
			substring.isdigit(),
			len(self.text) < 18
		)
		cursor_index = self.cursor_index()
		now_text = list(self.text)

		'''
		if now_text[cursor_index - 1] == '_':
			now_text[cursor_index - 1] = substring

		print(''.join(now_text), self.text)
		'''

		if all(true_conditions):
			self.text = ''.join(now_text)
			# return super().insert_text(substring, from_undo=from_undo)
# === Phone text input === #
# ======================== #


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


# =================== #
# === Color input === #
class _FDColorInputContent(BoxLayout):
	def get_value(self) -> tuple:
		return self.ids.color_picker.color

class FDColorInput(Popup):
	def __init__(self, title: str):
		self.title = title
		self.content = _FDColorInputContent()

		super().__init__(size_hint=(.9, .9))

		self.content.ids.accept_btn.bind(on_press=lambda e: print(self.get_value()))

	def get_value(self) -> tuple:
		return self.content.get_value()
# === Color input === #
# =================== #


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