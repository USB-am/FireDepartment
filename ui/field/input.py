from kivy.lang.builder import Builder
from kivy.properties import StringProperty
from kivymd.uix.textfield import MDTextField

from config import INPUT_FIELD


Builder.load_file(INPUT_FIELD)


class _BaseInput(MDTextField):
	'''
	Родительский класс виджетов ввода.

	~params:
	hint_text: str - placeholder.
	'''

	hint_text = StringProperty()

	def get_value(self) -> str:
		return self.text

	def set_value(self, text: str) -> None:
		self.text = text


class FDInput(_BaseInput):
	''' Поле ввода текста '''


class FDMultilineInput(_BaseInput):
	''' Поле ввода многострочного текста '''


class FDNumberInput(_BaseInput):
	''' Поле ввода целых чисел '''


class FDPhoneInput(_BaseInput):
	'''  Поле ввода номера телефона '''
