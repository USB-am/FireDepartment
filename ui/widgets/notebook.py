from typing import List
from collections.abc import Callable

from kivy.lang.builder import Builder # type: ignore
from kivymd.uix.boxlayout import MDBoxLayout # type: ignore
from kivymd.uix.label import MDLabel # type: ignore

from config import NOTEBOOK_WIDGET


Builder.load_file(NOTEBOOK_WIDGET)


class _NotebookMark(MDBoxLayout):
	''' Вкладка '''

	def __init__(self, title: str, **options):
		self.title = title
		self._active = False

		super().__init__(**options)

	@property
	def active(self) -> bool:
		return self._active

	@active.setter
	def active(self, state: bool) -> None:
		self._active = state

		if state:
			self.md_bg_color[-1] = .15
		else:
			self.md_bg_color[-1] = 0


class FDTab:
	''' Представление вкладки '''

	def __init__(self, title: str, content: MDBoxLayout):
		self._marker = _NotebookMark(title=title)
		self.content = content

	def bind_click(self, callback: Callable) -> None:
		''' Привязать событие к клику на вкладку '''

		self._marker.ids.tab_btn.bind(on_release=lambda instance: callback(instance))

	def bind_close(self, callback: Callable) -> None:
		''' Привязать событие к клику на крестик '''

		self._marker.ids.close_btn.bind(on_release=lambda instance: callback(instance))

	@property
	def title(self) -> str:
		return self._marker.title

	@title.setter
	def title(self, text: str) -> None:
		self._marker.title = text
		self._marker.ids.tab_btn.text = text

	@property
	def active(self) -> bool:
		return self._marker.active

	@active.setter
	def active(self, state: bool) -> None:
		self._marker.active = state


class FDNotebook(MDBoxLayout):
	''' Область с вкладками '''

	def __init__(self, **options):
		super().__init__(**options)
		self.current_tab = None
		self.__tabs: List[FDTab] = []

	def add_tab(self, tab: FDTab) -> None:
		''' Добавить вкладку '''

		self.__tabs.append(tab)

		tab.bind_click(lambda inst, t=tab: self.move_to_tab(t))
		tab.bind_close(lambda inst, t=tab: self.close_tab(t))
		self.ids.tab_list.add_widget(tab._marker)

		self.move_to_tab(tab)

	def move_to_tab(self, tab: FDTab) -> None:
		''' Переключиться на вкладку '''

		content_layout = self.ids.content
		for content in content_layout.children:
			content_layout.remove_widget(content)

		content_layout.add_widget(tab.content)
		self.current_tab = tab

		for tab in self.__tabs:
			tab.active = False
		self.current_tab.active = True

	def close_tab(self, tab: FDTab) -> None:
		''' Закрыть вкладку '''

		self.ids.tab_list.remove_widget(tab._marker)
		self.ids.content.remove_widget(tab.content)

		self.__tabs.remove(tab)

		if tab is self.current_tab:
			try:
				self.move_to_tab(self.__tabs[0])
			except IndexError:
				self.ids.content.add_widget(MDLabel(
					text='Ничего не выбрано', halign='center',
					valign='center'))
