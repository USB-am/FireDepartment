# -*- coding: utf-8 -*-

from app.tools.custom_widgets import CustomScreen
from kivymd.uix.label import MDLabel


class MainPage(CustomScreen):
	name = 'main_page'

	def __init__(self):
		super().__init__()

		self.add_widget(MDLabel(text='All good!', halign='center'))