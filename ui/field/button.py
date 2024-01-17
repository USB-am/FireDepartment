from typing import Callable, List, Dict

from kivy.lang.builder import Builder
from kivy.properties import StringProperty, ListProperty
from kivy.uix.anchorlayout import AnchorLayout
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.menu import MDDropdownMenu

from config import BUTTON_FIELD


Builder.load_file(BUTTON_FIELD)


class FDButton(MDBoxLayout):
	'''
	Иконка | Заголовок | Кнопка

	~params:
	icon: str - иконка;
	title: str - заголовок;
	btn_text: str - текст на кнопке.
	'''

	icon = StringProperty()
	title = StringProperty()
	btn_text = StringProperty()


class FDDoubleButton(MDBoxLayout):
	'''
	Заголовок | Кнопка | Кнопка

	~params:
	title: str - заголовок;
	btn1_text: str - текст на кнопке 1;
	btn2_text: str - текст на кнопке 2.
	'''

	title = StringProperty()
	btn1_text = StringProperty()
	btn2_text = StringProperty()


class FDIconButton(MDBoxLayout):
	'''
	Иконка | Заголовок | Кнопка (иконка)

	~params:
	icon: str - иконка;
	icon_btn: str - иконка на кнопке;
	title: str - заголовок.
	'''

	icon = StringProperty()
	icon_btn = StringProperty()
	title = StringProperty()

	def bind_btn(self, callback: Callable) -> None:
		'''
		Привязать событие к нажатию кнопки.

		~params:
		callback: Callable - событие, которое будет вызвано при нажатии.
		'''

		self.ids.btn.bind(on_release=lambda *_: callback())


class FDButtonDropdown(MDBoxLayout):
	'''
	Иконка | Заголовок | Выпадающий список

	~params:
	icon: str - иконка;
	title: str - заголовок;
	elems: List[str] - элементы списка.
	'''

	icon = StringProperty()
	title = StringProperty()
	elems = ListProperty([])

	def __init__(self, **params):
		super().__init__(**params)

		self.dropdown = MDDropdownMenu(
			caller=self.ids.btn,
			items=self.elems,
			width_mult=5
		)
		self.ids.btn.bind(on_release=lambda *_: self.dropdown.open())

	def update_elements(self, elements: List[Dict[str, str]]) -> None:
		''' Обновить содержимое выпадающего списка '''

		self.dropdown.items = elements


class FDRectangleButton(AnchorLayout):
	'''
	Широкая закрашенная кнопка.

	~params:
	title: str - текст на кнопке
	'''

	title = StringProperty()

	def bind_btn(self, callback: Callable) -> None:
		'''
		Привязать событие к нажатию кнопки.

		~params:
		callback: Callable - событие, которое будет вызвано при нажатии.
		'''

		self.ids.btn.bind(on_release=lambda *_: callback())