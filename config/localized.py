import os
import json


def write_new_localized_dict(path: str) -> None:
	dict_for_write = {
		'search': 'Поиск',
		'main': 'Главная',
		'options': 'Настройки',
		'create': 'Создать',
		'edit': 'Изменить',
		'current calls': 'Текущие вызовы',
		'position': 'Должность',
		'rank': 'Звание',
		'tag': 'Тег',
		'human': 'Человек',
		'emergency': 'Вызов',
		'ok': 'Ок',
		'title': 'Название',
		'stringfield': 'Поле ввода',
		'create tag': 'Добавить тег',
		'create rank': 'Добавить звание',
		'create position': 'Добавить должность',
		'create human': 'Добавить человека',
		'create emergency': 'Добавить вызов',
		'phone': 'Телефон',
		'addition phone': 'Дополнительный телефон',
		'work day': 'Рабочий день',
		'worktype': 'График работы',
		'description': 'Описание',
		'start work day': 'Начало рабочего дня',
		'finish work day': 'Конец рабочего дня',
		'work day range': 'Количество рабочих дней подряд',
		'week day range': 'Количество выходных дней подряд',
		'edit edit_tag_list list': 'Теги для редактирования',
		'edit edit_rank_list list': 'Звания для редактирования',
		'edit edit_position_list list': 'Должности для редактирования',
		'edit edit_human_list list': 'Люди для редактирования',
		'edit edit_emergency_list list': 'Вызовы для редактирования',
		'Edit edit_worktype_list list': 'Рабочие графики для редактирования',
		'urgent': 'Срочно',
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
			print(text)
			return text

		return output