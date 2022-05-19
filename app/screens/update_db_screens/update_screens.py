# -*- coding: utf-8 -*-

from kivy.uix.button import Button

from config import PATTERNS_DIR, LOCALIZED
from . import AbstractUpdateDBScreen
from data_base import db, Tag, Rank, Position, Human, Emergency, ColorTheme,\
	Worktype


class AbstractUpdateScreen(AbstractUpdateDBScreen):
	def __init__(self):
		super().__init__()

		self.update_title()

	def update_content(self, element: db.Model) -> None:
		super().update_content()
		self._element = element

		self.fill_fields()

		content = self.ids.content

		update_button = Button(
			size_hint=(1, None),
			size=(self.width, 60),
			text=LOCALIZED.translate('Update')
		)
		update_button.bind(on_release=self.update)
		content.add_widget(update_button)

	def fill_fields(self) -> None:
		for column_name, field in self.fields.items():
			element_column_value = getattr(self._element, column_name)
			field.set_value(element_column_value)

	def update(self, instance: Button) -> None:
		values = self.get_values()
		self.table.query.filter_by(id=self._element.id).update(values)


class EditTag(AbstractUpdateScreen):
	name = 'edit_tag'
	table = Tag


class EditRank(AbstractUpdateScreen):
	name = 'edit_rank'
	table = Rank


class EditPosition(AbstractUpdateScreen):
	name = 'edit_position'
	table = Position


class EditHuman(AbstractUpdateScreen):
	name = 'edit_human'
	table = Human


class EditEmergency(AbstractUpdateScreen):
	name = 'edit_emergency'
	table = Emergency


class EditColorTheme(AbstractUpdateScreen):
	name = 'edit_colortheme'
	table = ColorTheme


class EditWorkType(AbstractUpdateScreen):
	name = 'edit_worktype'
	table = Worktype