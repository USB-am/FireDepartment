from kivy.lang.builder import Builder
from kivy.properties import StringProperty
from kivymd.uix.boxlayout import MDBoxLayout

from config import LABEL_FIELD


Builder.load_file(LABEL_FIELD)


class FDTitle(MDBoxLayout):
	'''
	Заголовок.

	~params:
	title: str - текст заголовка.
	'''

	title = StringProperty()


class FDLabel(MDBoxLayout):
	'''
	Текстовое поле.

	~params:
	title: str - заголовок;
	value: str - текст.
	'''

	title = StringProperty()
	value = StringProperty()


class FDVerticalLabel(MDBoxLayout):
	'''
	Текстовое поле, где заголовок находится выше значения.

	~params:
	title: str - заголовок;
	value: str - текст.
	'''

	title = StringProperty()
	value = StringProperty()