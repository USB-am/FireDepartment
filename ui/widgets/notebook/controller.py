from typing import List, Any
import time
from collections import defaultdict

from kivymd.uix.textfield import MDTextField

from data_base import Human, Short


class _Logger(list):
	''' Логгер информации '''

	class __SubLog:
		def __init__(self, key: Any, value: Any):
			self.key = key
			self.value = value

		def __str__(self):
			return self.value

	def append(self, value: str) -> None:
		''' Записать лог '''

		super().append(self.__SubLog(
			key=time.time(),
			value=value
		))


class PhoneManager:
	''' Менеджер звонков '''

	__MESSAGES = ['', 'Вызов {human}', 'Неудачный вызов {human}']

	def __init__(self, humans: List[Human]):
		self._humans = humans
		self._control: defaultdict[Human.id, int] = defaultdict(lambda: 0)
		self.logger = _Logger()

	def call(self, human: Human) -> None:
		''' Сделать вызов сотруднику '''
		value = (self._control[human.id] + 1) % 3
		self._control[human.id] = value
		self.logger.append(PhoneManager.__MESSAGES[value].format(human=human))


class ShortManager(list):
	''' Менеджер сокращений '''
	def __init__(self, shorts: List[Short]):
		self._shorts = shorts
		self.logger = _Logger()

	def add(self, short: Short) -> None:
		''' Добавить сокращение '''
		self.append(short)
		self.logger.append(short.explanation)


class InformationManager:
	''' Менеджер дополнительной информации '''

	def __init__(self):
		self.logger = _Logger()

	def update(self, text: str) -> None:
		''' Обновить текст с дополнительной информацией '''
		self.logger.append(text)


class CallController:
	''' Контроллер Вызова '''

	def __init__(self, call: 'DataBase.Entry'):
		self._call = call
		self.phone_manager = PhoneManager(call.humans)
		self.short_manager = ShortManager(call.shorts)
		self.info_manager = InformationManager()

	def call_human(self, human: Human) -> None:
		''' Вызов сотрудника '''
		self.phone_manager.call(human)

	def add_short(self, short: Short) -> None:
		''' Добавить сокращение '''
		self.short_manager.add(short)

	def update_info_text(self, textfield: MDTextField) -> None:
		''' Обновить текст с дополнительной информацией '''
		self.info_manager.update(textfield.text)

	def __str__(self):
		global_logs = _Logger()
		global_logs.extend(self.phone_manager.logger)
		global_logs.extend(self.short_manager.logger)
		global_logs.extend(self.info_manager.logger)

		return '\n'.join(map(str, sorted(global_logs, key=lambda log: log.key)))
