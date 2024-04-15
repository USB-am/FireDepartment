

class FDTripleCheckbox:
	def __init__(self, title, substring, state=0):
		self.title = title
		self.substring = substring
		self.state = state

	def __str__(self):
		return f'[{self.state}] {self.title}'


class PhoneList(list):
	def __init__(self, *args, callback=lambda e: None):
		super().__init__(*args)
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

	def add_phones(self, *phones):
		self.phones.extend(*phones)


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
	print(*cc.call_manager.phone_manager.phones, sep='\n')
