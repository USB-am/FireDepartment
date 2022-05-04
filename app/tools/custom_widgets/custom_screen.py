# -*- coding: utf-8 -*-

from kivy.lang import Builder
from kivy.uix.screenmanager import Screen


KV = """
<CustomScreen>:
	canvas:
		Color:
			rgba: (1, 1, 1, 1)
		Rectangle:
			size: self.size
			pos: self.pos
			source: 'C:/Python/AndroidApps/FireDepartment/app/images/bg.png'
"""
Builder.load_string(KV)


class CustomScreen(Screen):
	pass