from kivy.lang.builder import Builder
from kivy.uix.screenmanager import Screen
from kivy.uix.widget import Widget

from app.path_manager import PathManager
from config import paths
from ui.widgets.toolbar import FDToolbar
from ui.frames.scrolled import FDScrolledFrame
from ui.frames.selection import FDSelectionFrame


Builder.load_file(paths.BASE_SCREEN)


class BaseScreen(Screen):
	''' Базовый экран '''

	color = (1, 1, 1, 1)
	bg_image = None

	def __init__(self):
		super().__init__()

		self.toolbar = FDToolbar(self.name)
		self.ids.widgets.add_widget(self.toolbar)

	def add_widgets(self, *widgets: Widget) -> None:
		'''
		Добавляет виджеты на экран.
		~params:
		: *widgets: Widget
		'''

		[self.ids.widgets.add_widget(widget) for widget in widgets]

	def clear(self) -> None:
		''' Очищает все содержимое '''

		container = self.id.widgets
		container.clear_widgets()


class BaseScrolledScreen(BaseScreen):
	''' Бозовый экран с прокрутной '''

	def __init__(self, *pre_scroll_widgets: Widget):
		super().__init__()

		for widget in pre_scroll_widgets:
			self.ids.widgets.add_widget(widget)

		self.scrolled_frame = FDScrolledFrame()
		self.ids.widgets.add_widget(self.scrolled_frame)

	def add_widgets(self, *widgets: Widget) -> None:
		self.scrolled_frame.add_widgets(*widgets)

	def clear(self) -> None:
		container = self.scrolled_frame.ids.content
		container.clear_widgets()


class SelectedScrollScreen(BaseScreen):
	''' Базовый экран с возможностью выбора элементов списка '''

	def __init__(self, *pre_scroll_widgets: Widget):
		super().__init__()

		for widget in pre_scroll_widgets:
			self.ids.widgets.add_widget(widget)

		self.selection_frame = FDSelectionFrame()
		self.selection_frame.ids.content.bind(
			on_selected=self._on_selected,
			on_unselected=self._on_unselected,
			on_selected_mode=self._set_selected_mode
		)
		self.ids.widgets.add_widget(self.selection_frame)

	def _set_selected_mode(self, instance_list: FDSelectionFrame,
		                  mode: bool) -> None:
		print(f'Mode is {mode}')
		if mode:
			left_items = [
				['close', lambda e: self.selection_frame.unselected_all()],
			]
			right_items = []
		else:
			left_items = [
				['bus', lambda e: print('All good!')],
			]
			right_items = []
			self.toolbar.title = 'All good!'

		self.toolbar.left_action_items = left_items
		self.toolbar.right_action_items = right_items

	def _on_selected(self, instance_list: FDSelectionFrame,
	                 instance_item) -> None:
		self.toolbar.title = str(
			len(instance_list.get_selected_list_items())
		)

	def _on_unselected(self, instance_list: FDSelectionFrame,
	                   instance_item) -> None:
		items_count = instance_list.get_selected_list_items()
		if items_count:
			self.toolbar.title = str(len(items_count))

	def add_widgets(self, *widgets: Widget) -> None:
		self.selection_frame.add_widgets(*widgets)

	def clear(self) -> None:
		container = self.selection_frame.ids.content
		container.clear_widgets()