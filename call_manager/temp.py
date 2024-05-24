from dataclasses import dataclass
from typing import List, Dict, Any
import time


# === TEMP === #
@dataclass
class Human:
	title: str
	phone: str

	id = 0
	def __new__(cls, *args, **kwargs):
		instance = super(Human, cls).__new__(cls)
		cls.id += 1
		instance.id = cls.id
		return instance

@dataclass
class Short:
	title: str
	text: str

@dataclass
class DBCall:
	title: str
	humans: List[Human]
	shorts: List[Short]

	def __str__(self):
		return self.title
# === TEMP === #


class _Logger(list):
	''' Логгер информации '''

	class __SubLog:
		def __init__(self, key: Any, value: Any):
			self.key = key
			self.value = value

	def append(self, value: str) -> None:
		''' Записать лог '''

		pass


class PhoneManager:
	''' Менеджер звонков '''
	def __init__(self, humans: List[Human]):
		self._humans = humans
		self._control: Dict[Human, int] = {human.id: 0 for human in humans}
		self.logger = _Logger()

	def call(self, human: Human) -> None:
		''' Сделать вызов сотруднику '''
		if human.id in self._control:
			self._control[human.id] = (self._control[human.id] + 1) % 3


class ShortManager:
	''' Менеджер сокращений '''
	def __init__(self, shorts: List[Short]):
		self._shorts = shorts


class InformationManager:
	''' Менеджер дополнительной информации '''


class Call:
	''' Вызов '''

	def __init__(self, call: 'DataBase.Entry'):
		self._call = call
		self.phone_manager = PhoneManager(call.humans)
		self.short_manager = ShortManager(call.shorts)
		self.info_manager = InformationManager()

	def call_human(self, human: Human) -> None:
		''' Вызов сотрудника '''
		self.phone_manager.call(human)


if __name__ == '__main__':
	hs = [Human(title=f'Human #{i+1}', phone=f'8 800 555 35 3{i}') for i in range(10)]
	ss = [Short(title=f'Short #{i+1}', text=f'Short text for Short #{i+1}') for i in range(10)]
	call_entry = DBCall(
		title='Call #1',
		humans=hs,
		shorts=ss
	)

	call = Call(call_entry)
