from kivy.lang.builder import Builder
from kivy.properties import StringProperty
from kivymd.uix.boxlayout import MDBoxLayout

from config import LABEL_FIELD


Builder.load_file(LABEL_FIELD)


class FDLabel(MDBoxLayout):
	'''
	Текстовое поле.

	~params:
	title: str - название поля;
	value: str - текст.
	'''

	title = StringProperty()
	value = StringProperty()