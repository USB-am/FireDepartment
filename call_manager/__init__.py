from typing import Type, List

from ui.widgets.triple_checkbox import FDTripleCheckbox


class PhoneProperty:
	def __init__(self, objtype: Type):
		self.objtype = objtype

	def __set_name__(self, owner, name):
		self.public_name = name
		self.private_name = '_' + name

	def __get__(self, instance, name):
		return instance.__dict__.get(self.private_name, name)

	def __set__(self, instance, value):
		if not isinstance(value, self.objtype):
			raise TypeError(f'{self.public_name} can only be of type {self.objtype.__class__.__name__}')

		instance.__dict__[self.private_name] = value


class Phone:
	''' Представление виджета с номером телефона '''

	phone_widget = PhoneProperty(FDTripleCheckbox)

	def __init__(self, phone_checkbox: FDTripleCheckbox):
		self.phone_widget = phone_checkbox

	def __str__(self):
		return self.phone_widget.title


class Phonebook:
	def __init__(self, phones: List[Phone]):
		self.phones = phones

	def __str__(self):
		return 'Phones:\n' + '\n'.join([f'- {str(phone)}' for phone in self.phones])


def test():
	ps = []
	for i in range(5):
		p = Phone(FDTripleCheckbox(
			normal_icon='bus',
			active_icon='eye',
			deactive_icon='bus',
			title=f'8800555353{i}'
		))
		ps.append(p)

	pb = Phonebook(ps)
	print(pb)
