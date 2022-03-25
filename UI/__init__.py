# -*- coding: utf-8 -*-

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager

from .main_page import MainPage
from .settings import Settings
from .edit_tables import EditTags, EditTag, EditPositions, EditPosition, EditRanks, \
	EditRank, EditPersons, EditPerson

# Temp import
from kivy.config import Config
Config.set('graphics', 'width', '350')


class Manager(ScreenManager):
	def __init__(self):
		super().__init__()

		self.add_widget(MainPage())
		self.add_widget(Settings())
		self.add_widget(EditTags())
		self.add_widget(EditTag())
		self.add_widget(EditRanks())
		self.add_widget(EditRank())
		self.add_widget(EditPositions())
		self.add_widget(EditPosition())
		self.add_widget(EditPersons())
		self.add_widget(EditPerson())

		self.current='main_page'


class FireDepartment(App):
	def build(self):
		manager = Manager()

		return manager