# -*- coding: utf-8 -*-

import os

from kivy.lang import Builder
from kivy.uix.button import Button

import config as Config
from .custom_screen import CustomScreen
from db_models import Post


path_to_kv_file = os.path.join(Config.PATTERNS_DIR, 'main_page.kv')
Builder.load_file(path_to_kv_file)


class PostItem(Button):
	def __init__(self, post):
		self.post = post
		self.view_text = self.post.title

		super().__init__()


class MainPage(CustomScreen):
	name = 'main_page'

	def __init__(self):
		super().__init__()

		self.bind(on_enter=self.fill_posts)

	def fill_posts(self, instance) -> None:
		container = self.ids.post_list
		container.clear_widgets()
		posts = Post.query.all()

		for post in posts:
			widget = PostItem(post)
			container.add_widget(widget)