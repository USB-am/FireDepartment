# -*- coding: utf-8 -*-

import os

from kivy.lang import Builder
from kivy.uix.button import Button
from kivymd.uix.list import TwoLineAvatarIconListItem, IconLeftWidget

from app.tools.custom_widgets import CustomScreen
from config import PATTERNS_DIR, LOCALIZED
from data_base import db, Tag, Rank, Position, Human, Emergency, ColorTheme,\
	Worktype


path_to_kv_file = os.path.join(PATTERNS_DIR, 'screens', 'update_list_db_screens.kv')
Builder.load_file(path_to_kv_file)


class ListElement(TwoLineAvatarIconListItem):
	def __init__(self, element: db.Model):
		self._element = element
		self.text = str(element)
		self.secondary_text = 'two list'
		self.table_icon = self._element.icon
		self.to_edit_screen = f'edit_{self._element.__tablename__.lower()}'

		super().__init__()

		self.add_widget(IconLeftWidget(icon=self.table_icon))


class AbstractUpdateListScreen(CustomScreen):
	def __init__(self):
		super().__init__()

		self.update_title()
		self.bind(on_pre_enter=self.update_content)

	def update_title(self) -> None:
		translate_text = LOCALIZED.translate(self.name)
		self.ids.toolbar.title = translate_text

	def update_content(self, instance: CustomScreen) -> None:
		elements = self.table.query.all()

		if not elements:
			return

		content = self.ids.content
		content.clear_widgets()

		for element in elements:
			content.add_widget(ListElement(element))


class UpdateListTag(AbstractUpdateListScreen):
	name = 'edit_tags'
	table = Tag


class UpdateListRank(AbstractUpdateListScreen):
	name = 'edit_ranks'
	table = Rank


class UpdateListPosition(AbstractUpdateListScreen):
	name = 'edit_positions'
	table = Position


class UpdateListHuman(AbstractUpdateListScreen):
	name = 'edit_humans'
	table = Human


class UpdateListEmergency(AbstractUpdateListScreen):
	name = 'edit_emergencys'
	table = Emergency


class UpdateListColorTheme(AbstractUpdateListScreen):
	name = 'edit_colorthemes'
	table = ColorTheme


class UpdateListWorkType(AbstractUpdateListScreen):
	name = 'edit_worktypes'
	table = Worktype