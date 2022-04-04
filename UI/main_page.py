# -*- coding: utf-8 -*-

import os

from kivy.lang import Builder
from kivy.uix.button import Button
from sqlalchemy import and_

import config as Config
from .custom_screen import CustomScreen
from db_models import db as DataBase
from db_models import Post, Tag


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

		self.ids.text_input.bind(on_text_validate=self.search)
		self.ids.search_btn.bind(on_press=self.search)
		self.bind(on_enter=self.fill_posts)

		self.ids.text_input.text = 'new;#2'
		self.search(None)

	def fill_posts(self, instance) -> None:
		container = self.ids.post_list
		container.clear_widgets()
		posts = Post.query.all()

		for post in posts:
			widget = PostItem(post)
			container.add_widget(widget)

	def fill_filter_posts(self, posts: list) -> None:
		container = self.ids.post_list
		container.clear_widgets()

		for post in posts:
			widget = PostItem(post)
			container.add_widget(widget)

	def __get_filter_posts(self, tags) -> list:
		result = set()
		filters = []

		for tag in tags:
			filters.append(Tag.title.contains(tag))

		filters_tags = Tag.query.filter(and_(*filters)).all()
		filter_posts = [filter_tag.posts for filter_tag in filters_tags]

		[result.add(post) for posts in filter_posts for post in posts]

		return sorted(list(result), key=lambda post: post.id)

	def search(self, instance) -> None:
		tags = map(lambda tag: tag.strip(), \
			self.ids.text_input.text.split(';'))

		filter_posts = self.__get_filter_posts(tags)

		self.fill_filter_posts(filter_posts)