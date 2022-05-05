# -*- coding: utf-8 -*-

import os


class PathManager:
	PATH = ['main_page']

	def forward(self, page_name: str) -> None:
		self.PATH.append(page_name)

	def back(self) -> str:
		if len(self.PATH) > 1:
			self.PATH = self.PATH[:-1]

		return self.get_current_page_name

	def get_current_page_name(self) -> str:
		return self.PATH[-1]


BASE_DIR = os.getcwd()
PATTERNS_DIR = os.path.join(BASE_DIR, 'app', 'kv')
IMAGES_DIR = os.path.join(BASE_DIR, 'app', 'images')
PATH_MANAGER = PathManager()