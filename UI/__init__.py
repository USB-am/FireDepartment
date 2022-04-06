# -*- coding: utf-8 -*-

# Temp import
from kivy.config import Config
Config.set("graphics", "resizable", "0")
Config.set('graphics', 'width', '350')

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager

from .main_page import MainPage
from .post_page import PostPage
from .settings import Settings
from .edit_list import EditTagList, EditRankList, EditPositionList, \
	EditPersonList, EditPostList
from .form import CreateTag, CreateRank, CreatePosition, CreatePerson, CreatePost, \
	EditTag, EditRank, EditPosition, EditPerson, EditPost


class Manager(ScreenManager):
	def __init__(self):
		super().__init__()

		# Main page
		self.add_widget(MainPage())
		self.add_widget(PostPage())

		# Settings page
		self.add_widget(Settings())

		# Edit list pages
		self.add_widget(EditTagList())
		self.add_widget(EditRankList())
		self.add_widget(EditPositionList())
		self.add_widget(EditPersonList())
		self.add_widget(EditPostList())

		# Create pages
		self.add_widget(CreateTag())
		self.add_widget(CreateRank())
		self.add_widget(CreatePosition())
		self.add_widget(CreatePerson())
		self.add_widget(CreatePost())

		# Edit pages
		self.add_widget(EditTag())
		self.add_widget(EditRank())
		self.add_widget(EditPosition())
		self.add_widget(EditPerson())
		self.add_widget(EditPost())

		self.current='edit_persons'


class FireDepartment(App):
	def build(self):
		manager = Manager()

		return manager