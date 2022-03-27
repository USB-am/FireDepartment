# -*- coding: utf-8 -*-

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager

from .main_page import MainPage
from .settings import Settings
from .edit_list import EditTagList, EditRankList, EditPositionList, \
	EditPersonList, EditPostList
# from .edit_tables import EditTags, EditTag, EditPositions, EditPosition, EditRanks, \
# 	EditRank, EditPersons, EditPerson

# Temp import
from kivy.config import Config
Config.set('graphics', 'width', '350')


class Manager(ScreenManager):
	def __init__(self):
		super().__init__()

		self.add_widget(MainPage())
		self.add_widget(Settings())
		self.add_widget(EditTagList())
		self.add_widget(EditRankList())
		self.add_widget(EditPositionList())
		self.add_widget(EditPersonList())
		self.add_widget(EditPostList())

		self.current='settings'


class FireDepartment(App):
	def build(self):
		manager = Manager()

		return manager