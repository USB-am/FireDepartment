# -*- coding: utf-8 -*-

from kivy.lang import Builder
from kivy.uix.screenmanager import Screen


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
	pass