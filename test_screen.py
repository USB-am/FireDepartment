# -*- coding: utf-8 -*-

from kivy.config import Config
Config.set("graphics", "resizable", "0")
Config.set('graphics', 'width', '350')

from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDTextButton

from settings import settings as Settings
from UI.fields.abstract__to_many_field import ForeignKeyField


class MyApp(MDApp):
	def build(self):
		bl = MDBoxLayout(orientation='vertical')
		f = ForeignKeyField('Person')
		b = MDTextButton(text='Get value')
		b.bind(on_press=lambda e: print(f.get_value()))

		bl.add_widget(f)
		bl.add_widget(b)

		return bl

MyApp().run()