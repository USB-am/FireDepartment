from kivymd.uix.textfield import MDTextField

from config import LOCALIZED


class StringField(MDTextField):
	''' Текстовое поле '''

	def __init__(self, title: str, **options):
		self.title = title

		super().__init__(size_hint=(1, None), size=(self.width, 50), **options)

		self.icon_right = 'form-textbox'
		self.hint_text = LOCALIZED.translate(title)

	def add_right_icon(self, icon: str) -> None:
		self.icon_right = icon

	def set_value(self, value: str) -> None:
		self.ids.entry.text = '-' if value is None else value

	def get_value(self) -> str:
		value = self.ids.entry.text

		return None if value == '-' else value


class PhoneField(StringField):
	''' Текстовое поле ввода телефона '''

	def __init__(self, title: str):
		super().__init__(title)

		self.add_right_icon('phone')


class DescriptionField(StringField):
	''' Многострочное поле '''

	def __init__(self, title: str):
		super().__init__(title, multiline=True, max_height=100)

		self.add_right_icon('text-long')


class IntegerField(StringField):
	''' Поле ввода целых чисел '''

	def __init__(self, title: str):
		super().__init__(title)

		self.add_right_icon('numeric')

	def insert_text(self, substring: str, from_undo=False) -> None:
		if substring.isdigit():
			super().insert_text(substring, from_undo=from_undo)