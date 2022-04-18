# -*- coding: utf-8 -*-

# Temp import
from kivy.config import Config
Config.set("graphics", "resizable", "0")
Config.set('graphics', 'width', '350')

from kivymd.app import MDApp

from .main_page import MainPage


class FireDepartment(MDApp):
	def build(self):
		return MainPage()