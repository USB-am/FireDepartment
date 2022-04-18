# -*- coding: utf-8 -*-

import os

from kivy.lang import Builder
from kivymd.uix.boxlayout import MDBoxLayout

from .custom_screen import CustomScreen
from settings import settings as Settings


path_to_kv_file = os.path.join(Settings.PATTERNS_DIR, 'main_page.kv')
Builder.load_file(path_to_kv_file)


class PostItem(MDBoxLayout):
	def __init__(self, title: str):
		self.title = title
		super().__init__()


class MainPage(CustomScreen):
	name = 'main_page'

	def __init__(self):
		super().__init__()

		self.update_posts()

	def update_posts(self, posts: list='all') -> None:
		if posts == 'all':
			for i in range(50):
				self.ids.container.add_widget(PostItem(
					title=f'Post #{i+1}'
				))
		print('Update posts is finished')