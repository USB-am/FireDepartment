# -*- coding: utf-8 -*-

import os

from kivy.lang import Builder
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.expansionpanel import MDExpansionPanel, MDExpansionPanelTwoLine

from .custom_screen import CustomScreen
from settings import settings as Settings
from db_models import Post


path_to_kv_file = os.path.join(Settings.PATTERNS_DIR, 'main_page.kv')
Builder.load_file(path_to_kv_file)


class PostItem(MDBoxLayout):
	pass


class MainPage(CustomScreen):
	name = 'main_page'

	def __init__(self):
		super().__init__()

		self.update_posts()

	def move_to_settings(self) -> None:
		self.manager.current = 'options'
		Settings.PATH_MANAGER.forward('options')

	def update_posts(self, posts: list='all') -> None:
		container = self.ids.container
		posts = Post.query.all()

		for post in posts:
			container.add_widget(MDExpansionPanel(
				icon='fire-alert',
				content=PostItem(),
				panel_cls=MDExpansionPanelTwoLine(
					text=post.title,
					secondary_text=post.description
				)
			))