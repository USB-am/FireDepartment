# -*- coding: utf-8 -*-

import os
import json


# Temp func
def create_localized_file() -> None:
	localized_dict = {
		'emergency': 'Черезвычайная ситуация',
		'human': 'Человек'
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
IMAGES_DIR = os.path.join(BASE_DIR, 'app', 'images')

LANG = 'ru'	# Temp variable (TODO: load from db)
create_localized_file()
LOCALIZED = _load_localized(LANG)
print(LOCALIZED)