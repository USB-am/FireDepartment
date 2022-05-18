# -*- coding: utf-8 -*-

from kivy.uix.button import Button

from . import AbstractUpdateDBScreen
from data_base import db, Tag, Rank, Position, Human, Emergency, ColorTheme,\
	Worktype
from config import LOCALIZED


class AbstractCreateScreen(AbstractUpdateDBScreen):
	def __init__(self):
		super().__init__()

		self.update_title()
		self.update_content()

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

	def create(self, instance: Button) -> bool:
		try:
			self.insert_values()
			super().clear_fields_content()
			# TODO: Вывести сообщение о успешном создании
			self.redirect_to_back_screen()

		except Exception as error:
			print('[{}] {}'.format(
				error.__class__.__name__,
				error
			))
			db.session.rollback()

	def insert_values(self) -> None:
		entered_values = self.get_values()
		element = self.table(**entered_values)

		db.session.add(element)
		db.session.commit()


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