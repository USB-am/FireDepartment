# -*- coding: utf-8 -*-

from kivy.lang import Builder
from kivy.uix.screenmanager import Screen

from app.tools.path_manager import PathManager


KV = """
#:import os os
#:import config config


<CustomScreen>:
	canvas:
		Color:
			rgba: (1, 1, 1, 1)
		Rectangle:
			size: self.size
			pos: self.pos
			source: os.path.join(config.IMAGES_DIR, 'bg.png')
"""
Builder.load_string(KV)


class CustomScreen(Screen):
	def redirect_to_back_screen(self) -> None:
		to_screen_name = PathManager.back()
		self.manager.current = to_screen_name