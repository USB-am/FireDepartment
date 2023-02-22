from kivy.lang.builder import Builder
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivy.properties import StringProperty

from config import paths


Builder.load_file(paths.SELECTED_LIST_FIELD)


class FDSelectList(MDBoxLayout):
	''' Список с checkbox'ами '''

	icon = StringProperty()
	title = StringProperty()

	def add(self, text: str) -> None:
		lst = self.ids.lst

		lst.add_widget(MDLabel(text=text, size_hint=(1, None), size=(self.width, 50)))