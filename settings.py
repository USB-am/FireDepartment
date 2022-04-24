# -*- coding: utf-8 -*-

import os
import json

from db_models import db as DataBase
from db_models import ColorTheme


LANG = {
	'Title': 'Название',
	'Name': 'ФИО',
	'Phone': 'Телефон',
	'Add_Phone': 'Телефон (Дополнительный)',
	'Work_Day': 'Рабочий день',
	'Work_Type': 'График работы',
	'Tag': 'Тег',
	'Tags': 'Теги',
	'Rank': 'Звание',
	'Ranks': 'Звания',
	'Position': 'Должность',
	'Positions': 'Должности',
	'Person': 'Человек',
	'Persons': 'Люди',
	'Post': 'Пост',
	'Posts': 'Посты',
	'Description': 'Описание'
}


def create_default_settings():
	# Create config.json file
	with open('config.json', mode='w', encoding='utf-8') as config_file:
		data = {
			'FONT_TITLE_SIZE': 20,
			'FONT_SIZE': 16,
			'NOW_COLOR_THEME_ID': 1
		}

		json.dump(data, config_file, indent=2)

	# Path to background image file
	path_to_default_bg = os.path.join(Settings.IMAGES_DIR, 'bg.png')

	# Add new color themes to data base
	dark = ColorTheme(
		title='Темная',
		button_color=(1, 1, 1, .3),
		font_color=(1, 1, 1, 1),
		background_color_opacity=(0, 0, 0, .5),
		background_image=path_to_default_bg
	)
	light = ColorTheme(
		title='Светлая',
		button_color=(0, 0, 0, .3),
		font_color=(0, 0, 0, 1),
		background_color_opacity=(1, 1, 1, .5),
		background_image=path_to_default_bg
	)

	DataBase.session.add_all([dark, light])
	DataBase.session.commit()


def check_exceptions(func):
	def wrapper(*args, **kwargs):
		try:
			return func(*args, **kwargs)

		except (AttributeError, FileNotFoundError):
			create_default_settings()
			return func(*args, **kwargs)

	return wrapper


class PathManager:
	def __init__(self):
		self.__global_path = ['main_page']

	@property
	def current(self) -> str:
		return self.__global_path[-1]

	def forward(self, page_name: str) -> None:
		self.__global_path.append(page_name)

	def back(self) -> str:
		if len(self.__global_path) > 1:
			self.__global_path = self.__global_path[:-1]

		return self.current


class Settings:
	BASE_DIR = os.getcwd()
	PATTERNS_DIR = os.path.join(BASE_DIR, 'UI', 'uix')
	IMAGES_DIR = os.path.join(BASE_DIR, 'UI', 'img')
	BACKGROUND_COLOR = (1, 1, 1, 0)
	ICONS = {
		'Tag': 'pound',
		'Rank': 'chevron-triple-up',
		'Position': 'crosshairs-gps',
		'Person': 'account-group',
		'Post': 'fire-alert',
		'Posts': 'fire-alert',
		'ColorTheme': 'palette',
		'Name': 'form-textbox',
		'Phone': 'phone',
		'Add_Phone': 'phone-plus',
		'Work_Type': 'calendar-multiselec',
	}

	def __init__(self):
		self.__dict__.update(self.__upload_config())
		self.__dict__.update(self.__upload_color_theme())
		self.INVERTED_FONT_COLOR = self.__invert_tuple(self.FONT_COLOR)
		self.INVERTED_BUTTON_COLOR = self.__invert_tuple(self.BUTTON_COLOR)
		self.PATH_MANAGER = PathManager()

	def update_config(self) -> None:
		data = {
			'FONT_TITLE_SIZE': self.FONT_TITLE_SIZE,
			'FONT_SIZE': self.FONT_SIZE,
			'NOW_COLOR_THEME_ID': self.NOW_COLOR_THEME_ID
		}

		with open('config.json', mode='w', encoding='utf-8') as config_file:
			json.dump(data, config_file, indent=2)

	def __invert_tuple(self, rgba: tuple) -> tuple:
		result = map(lambda c: 1 - c, rgba[:-1])

		return (*result, rgba[-1])

	@check_exceptions
	def __upload_config(self) -> dict:
		with open('config.json', mode='r', encoding='utf-8') as config_file:
			data = json.load(config_file)

		return data

	@check_exceptions
	def __upload_color_theme(self) -> dict:
		color_theme = ColorTheme.query.filter_by(id=self.NOW_COLOR_THEME_ID).first()

		return color_theme.get_values()

settings = Settings()