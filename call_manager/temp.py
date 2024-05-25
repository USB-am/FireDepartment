from dataclasses import dataclass
from typing import List, Dict, Any
import time
from collections import defaultdict


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

	def __str__(self):
		return self.title

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

		def __str__(self):
			return self.value

	def append(self, value: str) -> None:
		''' Записать лог '''

		log = self.__SubLog(key=time.time(), value=value)
		super().append(log)


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
		self.logger.append(short.text)


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

	def add_short(self, short: Short) -> None:
		''' Добавить сокращение '''
		self.short_manager.add(short)

	def __str__(self):
		output = ''
		output += '\n'.join(map(str, self.phone_manager.logger))
		output += '\n'.join(map(str, self.short_manager.logger))

		return output


if __name__ == '__main__':
	hs = [Human(title=f'Human #{i+1}', phone=f'8 800 555 35 3{i}') for i in range(10)]
	ss = [Short(title=f'Short #{i+1}', text=f'Short text for Short #{i+1}') for i in range(10)]
	call_entry = DBCall(
		title='Call #1',
		humans=hs,
		shorts=ss
	)

	call = Call(call_entry)
	call.call_human(hs[0])
	call.call_human(hs[0])
	call.add_short(ss[0])
	call.add_short(ss[3])
	call.add_short(ss[4])
	call.add_short(ss[1])
	print(call)
