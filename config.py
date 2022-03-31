# -*- coding: utf-8 -*-

import os


BASE_DIR = os.getcwd()
PATH_TO_DATA_BASE = 'sqlite:///file_department.db'
PATTERNS_DIR = os.path.join(BASE_DIR, 'UI', 'uix')
IMAGES_DIR = os.path.join(BASE_DIR, 'UI', 'img')

LANG = {
	'Title': 'Название',
	'Name': 'ФИО',
	'Phone': 'Телефон',
	'Add_Phone': 'Телефон 2',
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

THEME = True	# True - light theme; False - dark theme

FONT_TITLE_SIZE = 20
FONT_SIZE = 16

BUTTON_COLOR = (0, 0, 0, 1)
FONT_COLOR = (1, 1, 1, 1)
BACKGROUND_COLOR = (1, 1, 1, 1)
BACKGROUND_COLOR_OPACITY = (0, 0, 0, .5)
BACKGROUND_IMAGE = os.path.join(IMAGES_DIR, 'bg.png')

if not os.path.exists(BACKGROUND_IMAGE):
	BACKGROUND_IMAGE = None