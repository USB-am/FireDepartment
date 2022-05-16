# -*- coding: utf-8 -*-

from kivy.uix.button import Button
from kivymd.uix.boxlayout import MDBoxLayout

from . import AbstractUpdateDBScreen
from data_base import db, Tag, Rank, Position, Human, Emergency, ColorTheme,\
	Worktype
from config import LOCALIZED


class AbstractCreateScreen(AbstractUpdateDBScreen):
	def update_content(self) -> None:
		super().update_content()

		content = self.ids.content

		create_button = Button(
			size_hint=(1, None),
			size=(self.width, 60),
			text=LOCALIZED.translate('Create')
		)
		create_button.bind(on_press=self.create)
		self.ids.content.add_widget(create_button)

	def create(self, instance: Button) -> None:
		print(self.get_values())


class CreateTag(AbstractCreateScreen):
	name = 'create_tag'
	table = Tag


class CreateRank(AbstractCreateScreen):
	name = 'create_rank'
	table = Rank


class CreatePosition(AbstractCreateScreen):
	name = 'create_position'
	table = Position


class CreateHuman(AbstractCreateScreen):
	name = 'create_human'
	table = Human


class CreateEmergency(AbstractCreateScreen):
	name = 'create_emergency'
	table = Emergency


class CreateColorTheme(AbstractCreateScreen):
	name = 'create_colortheme'
	table = ColorTheme


class CreateWorkType(AbstractCreateScreen):
	name = 'create_worktype'
	table = Worktype