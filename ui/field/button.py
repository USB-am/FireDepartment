from typing import Callable

from kivy.lang.builder import Builder
from kivy.properties import StringProperty
from kivymd.uix.boxlayout import MDBoxLayout

from config import BUTTON_FIELD


Builder.load_file(BUTTON_FIELD)


class FDIconButton(MDBoxLayout):
	'''
	Иконка | Заголовок | Кнопка

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