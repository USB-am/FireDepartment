from os import path

from kivy.lang import Builder

from config import SCREENS_DIR, LOCALIZED
from app.tools import CustomScreen


from app.tools.fields.controllers import FDSwitch
from app.tools.fields.label import *
from kivy.uix.button import Button


path_to_kv_file = path.join(SCREENS_DIR, 'main_page.kv')
Builder.load_file(path_to_kv_file)


class Test:
	def __init__(self, title: str):
		self.title = title


class MainPage(CustomScreen):
	name = 'main_page'

	def __init__(self):
		super().__init__()

		s1 = FDTextArea('Content')
		s2 = FDTextArea('Human')
		s2.set_value('1. None\n2. True')
		self.ids.content.add_widget(s1)
		self.ids.content.add_widget(s2)
		b = Button(text='Check', size_hint=(1, None), size=(self.width, 70))
		b.bind(on_release=lambda e: print(s1.get_value()))
		self.ids.content.add_widget(b)