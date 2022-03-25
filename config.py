# -*- coding: utf-8 -*-

import os


BASE_DIR = os.getcwd()
PATH_TO_DATA_BASE = 'sqlite:///file_department.db'
PATTERNS_DIR = os.path.join(BASE_DIR, 'UI', 'uix')
IMAGES_DIR = os.path.join(BASE_DIR, 'UI', 'img')

LANG = {
	'Tag': 'Тег',
	'Rank': 'Звание',
	'Position': 'Должность',
	'Person': 'Человек',
	'Post': 'Пост'
}
BACKGROUND_COLOR = (1, 1, 1, 1)
BACKGROUND_IMAGE = 'C:/Users/CupkoRI/Desktop/bg.png'

if not os.path.exists(BACKGROUND_IMAGE):
	BACKGROUND_IMAGE = None