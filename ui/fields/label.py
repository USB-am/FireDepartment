from kivy.lang.builder import Builder
from kivy.properties import StringProperty
from kivymd.uix.boxlayout import MDBoxLayout

from config import paths


Builder.load_file(paths.LABEL_FIELD)


class FDLabel(MDBoxLayout):
	''' Поле с текстом '''

	title = StringProperty()
	value = StringProperty()