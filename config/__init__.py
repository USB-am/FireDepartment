# -*- coding: utf-8 -*-

import os
import json


# Temp func
def create_localized_file() -> None:
	localized_dict = {
		'main_page': 'Пожарка <3',
		'fires': 'Пахнет жареным',
		'options': 'Настройки',
		'colortheme': 'Персонализация',
		'create_tag': 'Новый тег',
		'create_emergency': 'Новое ЧС',
		'create_human': 'Новый человек',
		'create_rank': 'Новое звание',
		'create_position': 'Новая должность',
		'create_worktype': 'Новый график работы',
		'edit_tag_list': 'Теги',
		'edit_rank_list': 'Звания',
		'edit_position_list': 'Должности',
		'edit_human_list': 'Люди',
		'edit_emergency_list': 'ЧС',
		'edit_worktypes': 'Графики работы',
		'edit_tag': 'Редактирование тега',
		'edit_rank': 'Редактирование звания',
		'edit_position': 'Редактирование должности',
		'edit_human': 'Редактирование человека',
		'edit_emergency': 'Редактирование ЧС',
		'edit_worktype': 'Редактирование графика работы',
		'update_color_theme': 'Персонализация',
		'title': 'Название',
		'tag': 'Тег',
		'tags': 'Теги',
		'rank': 'Звание',
		'position': 'Должность',
		'human': 'Человек',
		'humans': 'Люди',
		'emergency': 'ЧС',
		'emergencys': 'ЧС',
		'worktype': 'График работы',
		'description': 'Описание',
		'urgent': 'Вызвать всех',
		'phone_1': 'Телефон',
		'phone_2': 'Доп. телефон',
		'work_day': 'Рабочий день',
		'start_work_day': 'Начало рабочего дня',
		'finish_work_day': 'Конец рабочего дня',
		'work_day_range': 'Рабочие дни подряд',
		'week_day_range': 'Выходные дни подряд',
		'create': 'Создать',
		'update': 'Обновить',
		'primary_hue': 'Оттенок',
		'primary_palette': 'Основная палитра',
		'accent_palette': 'Акцентирующий цвет',
		'theme_style': 'Тема',
		'background_image': 'Картинка заднего фона',
		'Light': 'Светлая',
		'Dark': 'Темная',
	}

	file = open(os.path.join(BASE_DIR, 'config', 'localized', 'ru.json'), mode='w')
	json.dump(localized_dict, file)
	file.close()


class ConfigDict(dict):
	def translate(self, text: str) -> str:
		return self.get(text.lower(), text)

	def __str__(self):
		result = '{\n'\
			+ ',\n'.join([f'\t"{key}": "{value}"' for key, value in self.items()])\
			+ '\n}'

		return result


def _load_localized(language: str) -> ConfigDict:
	file = open(
		os.path.join(BASE_DIR, 'config', 'localized', 'ru.json'),
		mode='r')
	result = json.load(file)
	file.close()

	return ConfigDict(result)


BASE_DIR = os.getcwd()
PATTERNS_DIR = os.path.join(BASE_DIR, 'app', 'kv')
TOOLS_DIR = os.path.join(PATTERNS_DIR, 'tools')
FIELDS_DIR = os.path.join(TOOLS_DIR, 'fields')
ADDITION_ELEMENTS_DIR = os.path.join(TOOLS_DIR, 'addition_elements')
SCREENS_DIR = os.path.join(PATTERNS_DIR, 'screens')
IMAGES_DIR = os.path.join(BASE_DIR, 'app', 'images')

LANG = 'ru'	# Temp variable (TODO: load from db)
create_localized_file()
LOCALIZED = _load_localized(LANG)