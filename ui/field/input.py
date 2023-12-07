from kivy.lang.builder import Builder
from kivy.properties import StringProperty
from kivymd.uix.textfield import MDTextField

from config import INPUT_FIELD


Builder.load_file(INPUT_FIELD)


class FDInput(MDTextField):
	'''
	Поле ввода текста.

	~params:
	hint_text: str - placeholder.
	'''

	hint_text = StringProperty()


class FDNumberInput(MDTextField):
	'''
	Поле ввода целых чисел.

	~params:
	hint_text: str - placeholder.
	'''

	hint_text = StringProperty()
