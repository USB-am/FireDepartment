# -*- coding: utf-8 -*-

import os

from kivy.lang import Builder
from kivy.uix.button import Button

import config as Config
from .custom_screen import CustomScreen
from db_models import db as DataBase
from db_models import Post


path_to_kv_file = os.path.join(Config.PATTERNS_DIR, 'main_page.kv')
Builder.load_file(path_to_kv_file)


class PostPage(CustomScreen):
	name = 'post_page'

	def __init__(self):
		super().__init__()


class PostItem(Button):
	def __init__(self, post):
		self.post = post
		self.view_text = self.post.title

		super().__init__()


class MainPage(CustomScreen):
	name = 'main_page'

	def __init__(self):
		super().__init__()

		self.ids.text_input.bind(on_text_validate=self.search)
		self.ids.search_btn.bind(on_press=self.search)
		self.bind(on_enter=self.fill_posts)

	def fill_posts(self, instance) -> None:
		container = self.ids.post_list
		container.clear_widgets()
		posts = Post.query.all()

		for post in posts:
			widget = PostItem(post)
			container.add_widget(widget)

	def search(self, instance) -> None:
		tags = map(lambda tag: tag.strip(), \
			self.ids.text_input.text.split(';'))

		for tag in tags:
			search_text = f'%{tag}%'
			print(type(Post.tags), Post.tags, dir(Post.tags))
			print(Post.tags.like('%new%'))
			# print(Post.tags.like(search_text), end='\n'*5)
			# print(Post.query.filter(Post.tags.all().filter(search_text)).all())
			# print(DataBase.session.query(Post).filter(Post.tags.like(search_text)))