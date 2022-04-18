# -*- coding: utf-8 -*-

# Temp import
from kivy.config import Config
Config.set("graphics", "resizable", "0")
Config.set('graphics', 'width', '350')

from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager

from .main_page import MainPage
from .options import Options


class Manager(ScreenManager):
	def __init__(self):
		super().__init__()

		# Main page
		self.add_widget(MainPage())

		# Options
		self.add_widget(Options())

		self.current = 'options'


class FireDepartment(MDApp):
	def build(self):
		return Manager()