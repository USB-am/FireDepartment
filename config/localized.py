import os
import json


def write_new_localized_dict(path: str) -> None:
	dict_for_write = {
		'search': 'Поиск',
		'main': 'Главная',
		'options': 'Настройки',
		'create': 'Создать',
		'edit': 'Изменить',
	}

	with open(path, mode='w') as writed_file:
		json.dump(dict_for_write, writed_file, indent=2)


class JsonReader(dict):
	def __init__(self, path_to_json_file: str):
		super().__init__()

		write_new_localized_dict(path_to_json_file)
		self.path_to_json_file = path_to_json_file

	def read(self) -> dict:
		with open(self.path_to_json_file, mode='r') as translate_file:
			result = json.load(translate_file)

		return result


class Localized:
	def __init__(self, path_to_localized_file: str):
		self.vocabulary = JsonReader(path_to_localized_file).read()

	def translate(self, text: str) -> str:
		output = self.vocabulary.get(text.lower())

		if output is None:
			return text

		return output