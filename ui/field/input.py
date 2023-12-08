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


class FDInput(_BaseInput):
	''' Поле ввода текста '''


class FDNumberInput(_BaseInput):
	''' Поле ввода целых чисел '''


class FDPhoneInput(_BaseInput):
	'''  Поле ввода номера телефона '''
