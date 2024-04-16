from typing import Any


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

		if value % 3 > 3:
			value = value % 3

		self._state = value

	def __str__(self):
		if self.state == 0:
			return f'Neutral {self.title}'
		elif self.state == 1:
			return f'Selected {self.title}'
		elif self.state == 2:
			return f'Unselected {self.title}'


class PhoneLogger(dict):
	def add_log(self, obj: Any, status: str) -> None:
		if obj in self:
			self[id(obj)].append(status)
		else:
			self[id(obj)] = [status,]

	def __str__(self):
		output = ''
		for key, logs in self.items():
			output += str(key) + ', '.join(logs) + '\n'

		return output


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
		self.logger = PhoneLogger()

	def add_phones(self, *phones):
		self.phones.extend(phones)

	def select_phone(self, phone: FDTripleCheckbox) -> None:
		if phone not in self:
			self.add_phones(phone)

		phone.state += 1
		self.logger.add_log(phone, str(phone))


class CallManager:
	def __init__(self, phones):
		self.phone_manager = PhoneManager(*phones)

	def add_phone(self, phone):
		self.phone_manager.add_phone(phone)


class CallController:
	def __init__(self, boxlayout):
		self.boxlayout = boxlayout
		self.call_manager = CallManager(boxlayout.phones)


def get_all_checkboxes():
	return [FDTripleCheckbox(
		title=f'Phone #{i+1}',
		substring=f'Substring #{i+1}',
		state=i%3) for i in range(50)
	]

class BoxLayout_:
	def __init__(self):
		self.phones = get_all_checkboxes()


if __name__ == '__main__':
	boxlayout = BoxLayout_()
	cc = CallController(boxlayout)
	pm = cc.call_manager.phone_manager
	print(*pm, sep='\n')
