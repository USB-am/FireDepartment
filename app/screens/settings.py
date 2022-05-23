# -*- coding: utf-8 -*-

import os

from kivy.lang import Builder
from kivymd.uix.boxlayout import MDBoxLayout

from app.tools.custom_widgets import CustomScreen, FDExpansionPanel
from config import PATTERNS_DIR, LOCALIZED
from data_base import Tag, Rank, Position, Human, Emergency, \
	Worktype, ColorTheme


path_to_kv_file = os.path.join(PATTERNS_DIR, 'screens', 'settings.kv')
Builder.load_file(path_to_kv_file)


class DataBaseElement(MDBoxLayout):
	def __init__(self, db_model_obj):
		self.db_model_obj = db_model_obj
		self.to_create_screen_name = 'create_{}'.format(
			self.db_model_obj.__tablename__.lower())
		self.to_edit_screen_name = 'edit_{}s'.format(
			self.db_model_obj.__tablename__.lower())

		super().__init__()


class ColorThemeElement(MDBoxLayout):
	pass


class Settings(CustomScreen):
	name = 'settings'

	def __init__(self):
		super().__init__()

		self.update_title()
		self.update_content()

	def update_title(self) -> None:
		translate_text = LOCALIZED.translate('Settings')
		self.ids.toolbar.title = translate_text

	def update_content(self) -> None:
		content = self.ids.content
		content.clear_widgets()

		data_bases = (Tag, Rank, Position, Human, Emergency,
			Worktype)#, ColorTheme)

		for db_model in data_bases:
			content.add_widget(FDExpansionPanel(
				db_model=db_model,
				content=DataBaseElement,
				text=(db_model.__tablename__, )
			))

		content.add_widget(ColorThemeElement())