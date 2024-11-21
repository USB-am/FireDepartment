from kivy.lang.builder import Builder
from kivy.uix.screenmanager import Screen
from kivy.uix.widget import Widget

from app.path_manager import PathManager
from config import BASE_SCREEN


Builder.load_file(BASE_SCREEN)


class _FDScreen(Screen):
	''' Родитель для базовых классов страниц '''

	def __init__(self, path_manager: PathManager):
		super().__init__()

		self._path_manager = path_manager

	def add_content(self, widget: Widget) -> None:
		'''
		Добавляет виджет на страницу.

		~params:
		widget: Widget - любой элемент, который можно отобразить через
			метод add_widget.
		'''

		self.ids.content.add_widget(widget)

	def clear_content(self) -> None:
		''' Очищает содержимое поля с контентом '''

		self.ids.content.clear_widgets()

	def open_menu(self, *events) -> None:
		''' Открывает боковое меню. '''

		self.parent.parent.ids.menu.set_state('open')


class BaseScreen(_FDScreen):
	''' Базовое представление страницы (без прокрутки). '''


class BaseScrollScreen(_FDScreen):
	''' Базовое представление страницы (с прокруткой). '''

	def end_list_event(self) -> None:
		''' Событие прокрутки до конца страницы '''


class BaseSelectScrollScreen(_FDScreen):
	''' Базовое представление страницы (с прокруткой и возможности выбора) '''

	def end_list_event(self) -> None:
		''' Событие прокрутки до конца страницы '''

	def on_selected(self, instance_selection_list, instance_selection_item) -> None:
		''' Обработчик события выбора '''

	def on_unselected(self, instance_selection_list, instance_selection_item) -> None:
		''' Обработчик события снятия выбора '''

	def set_selection_mode(self, instance_selection_list, mode) -> None:
		''' Определение поведения при выборе '''
