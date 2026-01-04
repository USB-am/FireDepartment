from kivy.lang.builder import Builder
from kivy.uix.widget import Widget
from kivy.properties import StringProperty
from kivymd.uix.boxlayout import MDBoxLayout

from config import LABEL_LAYOUT


Builder.load_file(LABEL_LAYOUT)


class FDLabelLayout(MDBoxLayout):
	''' Поле с надписью сверху '''

	label = StringProperty()

	def add_content(self, widget: Widget) -> None:
		''' Добавить элемент '''

		self.ids.content.add_widget(widget)
