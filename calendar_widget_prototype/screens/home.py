from kivy.uix.screenmanager import Screen
from kivy.lang.builder import Builder
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel

from config import HOME_KV
from ui.fields.calendar import FDCalendar


Builder.load_file(HOME_KV)


class HomeScreen(Screen):
	name = 'home'

	def __init__(self, **kw):
		super().__init__(**kw)
		self.ids.content.orientation = 'vertical'

		calendar_ = FDCalendar()
		self.ids.content.add_widget(calendar_)
		self.ids.content.add_widget(MDBoxLayout(size_hint=(1, 1), md_bg_color=(1, 1, 1, 1)))
