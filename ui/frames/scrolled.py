import os

from kivy.lang import Builder
from kivy.uix.scrollview import ScrollView

from config import paths


Builder.load_file(paths.SCROLLED_FRAME)


class FDScrolledFrame(ScrollView):
	''' Область прокрутки '''

	def add_widgets(self, *widgets) -> None:
		[self.ids.content.add_widget(widget) for widget in widgets]