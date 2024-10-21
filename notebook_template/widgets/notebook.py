from typing import List
from collections.abc import Callable

from kivy.lang.builder import Builder
from kivymd.uix.boxlayout import MDBoxLayout

from config import NOTEBOOK_WIDGET_KV


Builder.load_file(NOTEBOOK_WIDGET_KV)


class _NotebookMark(MDBoxLayout):
	''' Вкладка '''

	def __init__(self, title: str, **options):
		self.title = title

		super().__init__(**options)


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


class FDNotebook(MDBoxLayout):
	''' Область с вкладками '''

	def __init__(self, **options):
		super().__init__(**options)
		self.__tabs: List[FDTab] = []

		for i in range(30):
			txt = f'Tab #{i+1}'
			content = MDBoxLayout()
			tab = FDTab(title=txt, content=content)
			self.add_tab(tab)

	def add_tab(self, tab: FDTab) -> None:
		''' Добавить вкладку '''

		tab.bind_click(lambda inst: print(inst.parent.title))
		tab.bind_close(lambda inst: print(f'Click by close {inst}'))
		self.ids.tab_list.add_widget(tab._marker)
