# -*- coding: utf-8 -*-

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager

from .main_page import MainPage
from .settings import Settings

# Temp import
from kivy.config import Config
Config.set('graphics', 'width', '350')


class Manager(ScreenManager):
	def __init__(self):
		super().__init__()

		self.add_widget(MainPage())
		self.add_widget(Settings())


class FireDepartment(App):
	def __init__(self):
		super().__init__()

		self.manager = Manager()
		self.manager.add_widget(MainPage())

	def build(self):
		return self.manager