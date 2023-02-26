from kivy.lang import Builder
from kivy.uix.scrollview import ScrollView

from config import paths


Builder.load_file(paths.SELECTION_FRAME)


class FDSelectionFrame(ScrollView):
	''' Область выбора '''

	def add_widgets(self, *widgets) -> None:
		[self.ids.content.add_widget(widget) for widget in widgets]