from kivy.lang.builder import Builder
from kivy.properties import StringProperty
from kivymd.uix.boxlayout import MDBoxLayout

from config import HISTORY_LAYOUT


Builder.load_file(HISTORY_LAYOUT)


class FDHistoryElement(MDBoxLayout):
	''' Элемент на экране history '''

	title = StringProperty()
