# -*- coding: utf-8 -*-

import re
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


def check_exceptions(func):
	def wrapper(*args, **kwargs):
		try:
			return func(*args, **kwargs)
		except IndexError:
			pass
		except Exception as exception:
			print(exception)
	return wrapper


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
	_COMPLITE_PATTERN = r'\+?[78](\d{3})(\d{3})(\d{2})(\d{2})'
	_NOT_COMPLITE_PATTERN = r'\+?[78]([0-9_]{3})([0-9_]{3})([0-9_]{2})([0-9_]{2})'
	_REPL = r'+7 (\1) \2-\3-\4'

	def __init__(self, **options):
		super().__init__(**options)

		self.text = self.MASK
		self.wrapper_number = '7495'.ljust(11, '_')

	def keyboard_on_key_down(self, window, keycode, text, modiriers) -> None:
		if keycode[1] in ('backspace', 'delete'):
			return

		return super().keyboard_on_key_down(window, keycode, text, modiriers)

	@check_exceptions
	def insert_text(self, substring: str, from_undo: bool=False) -> None:
		if not substring.isdigit():
			return

		cursor_index = self.__get_cursor_index()
		if cursor_index == -1:
			return

		now_text_list = list(self.text)
		now_text_list[cursor_index] = substring
		now_text = ''.join(now_text_list)
		self.wrapper_number = ''.join(re.findall(r'[\d_]*', now_text))

		self.text = re.sub(self._NOT_COMPLITE_PATTERN, self._REPL, self.wrapper_number)
		self.cursor = (self.__get_cursor_index(), 0)

	def __get_cursor_index(self) -> int:
		cursor_index = self.cursor_index()

		if cursor_index == len(self.text):
			cursor_index = self.text.find('_')

		return cursor_index

	def set_value(self, phone_number: str) -> None:
		self.wrapper_number = phone_number
		self.text = re.sub(self._COMPLITE_PATTERN, self._REPL, self.wrapper_number)
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