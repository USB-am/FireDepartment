from kivy.lang.builder import Builder
from kivy.properties import StringProperty, ListProperty
from kivymd.uix.textfield import MDTextField

from config import INPUT_FIELD


Builder.load_file(INPUT_FIELD)


class _BaseInput(MDTextField):
	'''
	Родительский класс виджетов ввода.

	~params:
	hint_text: str - placeholder;
	validators: list=[] - список валидаторов при вводе.
	'''

	hint_text = StringProperty()
	validators = ListProperty([])

	def get_value(self) -> str:
		return self.text

	def set_value(self, text: str) -> None:
		self.text = text

	def on_text(self, instance, text):
		for validator in self.validators:
			check = validator(text)
			if not check.status:
				self.error = True
				self.helper_text = check.text
				break
		else:
			self.error = False
			self.helper_text = ''


class FDInput(_BaseInput):
	''' Поле ввода текста '''


class FDMultilineInput(_BaseInput):
	''' Поле ввода многострочного текста '''


class FDNumberInput(_BaseInput):
	''' Поле ввода целых чисел '''


class FDPhoneInput(_BaseInput):
	'''  Поле ввода номера телефона '''
