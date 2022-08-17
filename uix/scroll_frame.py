import os

from kivy.lang import Builder
from kivy.uix.scrollview import ScrollView


path_to_kv_file = os.path.join(os.getcwd(), 'kv', 'uix', 'scroll_frame.kv')
Builder.load_file(path_to_kv_file)


class FDScrollFrame(ScrollView):
	''' Область прокрутки '''

	def add_widgets(self, *widgets) -> None:
		[self.ids.content.add_widget(widget) for widget in widgets]