# -*- coding: utf-8 -*-

from db_models import Post


class Filter:
	def __init__(self, posts: list):
		self.posts = posts