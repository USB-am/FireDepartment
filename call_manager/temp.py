from typing import Any
from datetime import datetime


class FDTripleCheckbox:
	def __init__(self, title, substring, state=0):
		self.title = title
		self.substring = substring
		self._state = state

	@property
	def state(self) -> int:
		return self._state

	@state.setter
	def state(self, value: int) -> None:
		if not isinstance(value, int):
			raise AttributeError

		if value >= 3:
			value = value % 3

		self._state = value

	def __str__(self):
		if self.state == 0:
			return f'Neutral {self.title}'
		elif self.state == 1:
			return f'Selected {self.title}'
		elif self.state == 2:
			return f'Unselected {self.title}'


class Short:
	def __init__(self, title: str, explanation: str):
		self.title = title
		self.explanation = explanation

	def __str__(self):
		return self.title


class LogElement:
	def __init__(self, msg: str):
		self.msg = msg
		self.timestamp = datetime.now().strftime('[%H:%M:%S %d.%m.%Y]')

	def __str__(self):
		return f'{self.timestamp} {self.msg}'


class Logger(dict):
	def add_log(self, obj: Any, msg: str) -> None:
		log = LogElement(msg)
		obj_id = id(obj)

		if obj_id in self:
			self[obj_id].append(log)
		else:
			self[obj_id] = [log,]

	def _all_logs(self) -> str:
		output = ''
		for key, logs in self.items():
			output += str(key) + ' '  + ', '.join(map(str, logs)) + '\n'

		return output

	def __str__(self):
		return '\n'.join([f'{key} {logs[-1]}' for key, logs in self.items()])


# === PHONE MANAGER === #
class PhoneList(list):
	def __init__(self, *args, callback=lambda e: None):
		super().__init__(args)
		self.callback = callback

	def append(self, elem) -> None:
		super().appned(elem)
		self.callback(elem)

	def extend(self, *elems) -> None:
		super().extend(elems)
		self.callback(*elems)


class PhoneManager(PhoneList):
	def __init__(self, *phones):
		super().__init__(*phones)
		self.logger = Logger()

	def add_phones(self, *phones):
		self.extend(phones)

	def select_phone(self, phone: FDTripleCheckbox) -> None:
		if phone not in self:
			self.add_phones(phone)

		phone.state += 1
		self.logger.add_log(phone, str(phone))
# === PHONE MANAGER === #


# === SHORTS MANAGER === #
class ShortsList(list):
	def __init__(self, *args, callback=lambda e: None):
		super().__init__(args)
		self.callback = callback

	def append(self, elem) -> None:
		super().append(elem)
		self.callback(elem)

	def extend(self, *elems) -> None:
		super().extend(elems)
		self.callback(*elems)


class ShortsManager(ShortsList):
	def __init__(self, *shorts):
		super().__init__(*shorts)
		self.logger = Logger()

	def add_shorts(self, *shorts: Short) -> None:
		self.extend(shorts)

	def select_short(self, short) -> None:
		if short not in self:
			self.add_shorts(short)

		self.logger.add_log(short, str(short))
# === SHORTS MANAGER === #

# === TEXT MANAGER === #
class TextList(list):
	pass


class TextManager(TextList):
	def __init__(self, textfield):
		self.textfield = textfield
		self.logger = Logger()

	def __add__(self, msg: str):
		self.textfield.text += msg
		self.logger.add_log(self, msg)
# === TEXT MANAGER === #


class CallManager:
	def __init__(self, phones):
		self.phone_manager = PhoneManager(*phones)
		self.shorts_manager = ShortsManager(emergency.shorts)
		self.text_manager = TextManager()

	def add_phone(self, phone):
		self.phone_manager.add_phone(phone)

	def add_short(self, short):
		self.shorts_manager.add_shorts(short)

	def __str__(self):
		return str(self.shorts_manager.logger)


class CallController:
	def __init__(self, emergency, boxlayout):
		self.boxlayout = boxlayout
		self.call_manager = CallManager(boxlayout.phones)

	def select_phone(self, phone: FDTripleCheckbox) -> None:
		self.call_manager.phone_manager.select_phone(phone)

	def select_short(self, short: Short) -> None:
		self.call_manager.shorts_manager.select_short(short)


def get_all_checkboxes():
	return [FDTripleCheckbox(title=f'Phone #{i+1}',
	                         substring=f'Substring #{i+1}',
	                         state=0)
		for i in range(50)
	]

class BoxLayout_:
	phones = get_all_checkboxes()


def gen_shorts():
	return [Short(
	              title=f'Short #{2**i}',
	              explanation=f'Explanation for Short #{2**i}')
		for i in range(10)
	]

class Emergency:
	def __init__(self, title, shorts: list):
		self.title = title
		self.shorts = shorts

	def __str__(self):
		return self.title


if __name__ == '__main__':
	boxlayout = BoxLayout_()
	emergency = Emergency('Emergency #1', gen_shorts())
	cc = CallController(emergency, boxlayout)
	cc.select_short(emergency.shorts[0])
	cc.select_short(emergency.shorts[0])
	cc.select_short(emergency.shorts[1])
	cc.select_short(emergency.shorts[2])
	print(cc.call_manager)

	# cc.select_phone(BoxLayout_.phones[0])
	# cc.select_phone(BoxLayout_.phones[0])
	# cc.select_phone(BoxLayout_.phones[0])
	# cc.select_phone(BoxLayout_.phones[1])
	# cc.select_phone(BoxLayout_.phones[2])
	# print(cc.call_manager)
