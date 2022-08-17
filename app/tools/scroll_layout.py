from os import path

from kivy.lang import Builder
from kivy.uix.scrollview import ScrollView

from config import TOOLS_DIR


path_to_kv_file = path.join(TOOLS_DIR, 'scroll_layout.kv')
Builder.load_file(path_to_kv_file)


class FDScrollLayout(ScrollView):
	''' Виджет прокрутки '''
	def add_widgets(self, *widgets) -> None:
		[self.ids.content.add_widget(widget) for widget in widgets]