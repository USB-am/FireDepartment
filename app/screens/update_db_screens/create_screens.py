# -*- coding: utf-8 -*-

from kivymd.uix.boxlayout import MDBoxLayout

from . import AbstractUpdateDBScreen
from data_base import Tag, Rank, Position, Human, Emergency, ColorTheme,\
	WorkType


class AbstractCreateScreen(AbstractUpdateDBScreen):
	pass


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
	table = WorkType