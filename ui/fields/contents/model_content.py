from os.path import join as pjoin
from typing import Callable

from kivy.lang.builder import Builder
from kivymd.uix.boxlayout import MDBoxLayout

from config.paths import __CONTENT_DIR


Builder.load_file(pjoin(__CONTENT_DIR, 'model_content.kv'))


class EmergencyModelContent(MDBoxLayout):
	''' Виджеты, используемые при создании/редактирования Emergency '''

	def add_submit(self, *, text: str, callback: Callable) -> None:
		pass
