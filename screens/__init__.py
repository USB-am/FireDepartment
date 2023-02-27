from kivy.lang.builder import Builder
from kivy.uix.screenmanager import Screen
from kivy.uix.widget import Widget
from kivymd.uix.bottomnavigation import MDBottomNavigationItem

from app.path_manager import PathManager
from config import paths
from ui.widgets.toolbar import FDToolbar
from ui.frames.scrolled import FDScrolledFrame
from ui.frames.selection import FDSelectionFrame

from kivymd.uix.boxlayout import MDBoxLayout


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


class FDBottomNavigation(MDBoxLayout):
	pass

class BaseBottomNavigationScreen(BaseScreen):
	''' Базовый экран с нижней полосой навигации '''

	def __init__(self):
		super().__init__()

		self.bottom_navigation = FDBottomNavigation()
		super().add_widgets(self.bottom_navigation)

	def add_widgets(self, *navigation_items: MDBottomNavigationItem) -> None:
		[self.bottom_navigation.ids.nav.add_widget(item) \
			for item in navigation_items]

	def clear(self) -> None:
		container = self.bottom_navigation.ids.nav
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
			on_unselected=self._on_unselected
		)
		self.ids.widgets.add_widget(self.selection_frame)
		self.__toolbar_data = {
			'title': self.toolbar.title,
			'left_action_items': self.toolbar.left_action_items,
			'right_action_items': self.toolbar.right_action_items,
		}

	def _set_selected_mode(self, mode: bool) -> None:
		if mode:
			left_items = [
				['close', lambda e: self.selection_frame.unselected_all()],
			]
			right_items = []
		else:
			left_items = self.__toolbar_data['left_action_items']
			right_items = self.__toolbar_data['right_action_items']
			self.toolbar.title = self.__toolbar_data['title']

		self.toolbar.left_action_items = left_items
		self.toolbar.right_action_items = right_items

	def _on_selected(self, instance_list: FDSelectionFrame,
	                 instance_item) -> None:
		self.toolbar.title = str(
			len(instance_list.get_selected_list_items())
		)
		self._set_selected_mode(True)

	def _on_unselected(self, instance_list: FDSelectionFrame,
	                   instance_item) -> None:
		items_count = instance_list.get_selected_list_items()
		if items_count:
			self.toolbar.title = str(len(items_count))
		
		self._set_selected_mode(bool(items_count))

	def add_widgets(self, *widgets: Widget) -> None:
		self.selection_frame.add_widgets(*widgets)

	def clear(self) -> None:
		container = self.selection_frame.ids.content
		container.clear_widgets()