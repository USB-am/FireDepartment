from typing import Callable

from kivy.lang.builder import Builder
from kivy.properties import StringProperty
from kivy.uix.anchorlayout import AnchorLayout
from kivymd.uix.boxlayout import MDBoxLayout

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