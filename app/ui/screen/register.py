from kivy.lang.builder import Builder
from kivymd.uix.boxlayout import MDBoxLayout

from path_manager import PathManager
from .based_screen import BaseScreen
from ui.widgets.text_input import FDTextInput, FDPasswordInput
from ui.widgets.choice import FDChoice
from validators import EmptyValidator


class FDRegisterScreen(BaseScreen):
	name = 'register'
	title = 'Регистрация'

	def __init__(self, path_manager: PathManager):
		super().__init__(path_manager)
		self.ids.toolbar.anchor_title = 'center'
		self.add_left_toolbar_items('arrow-left', lambda *_: self.path_manager.back())

	def on_pre_enter(self, *args) -> None:
		self.clear_content()

		self.email_field = FDTextInput(
			hint_text='Электронная почта',
			validators=[
				EmptyValidator(error_msg='Поле не может быть пустым!'),
			]
		)
		self.add_content(self.email_field)

		self.username_field = FDTextInput(
			hint_text='Имя пользователя',
			validators=[
				EmptyValidator(error_msg='Поле не может быть пустым!'),
			]
		)
		self.add_content(self.username_field)

		self.pwd_field = FDPasswordInput(
			hint_text='Пароль',
			validators=[
				EmptyValidator(error_msg='Поле не может быть пустым!'),
			]
		)
		self.add_content(self.pwd_field)

		self.pwd_again_field = FDPasswordInput(
			hint_text='Пароль (повтор)',
			validators=[
				EmptyValidator(error_msg='Поле не может быть пустым!')
			]
		)
		self.add_content(self.pwd_again_field)

		self.fire_department_field = FDChoice(
			hint_text='Номер части',
			validators=[
				EmptyValidator(error_msg='Поле не может быть пустым!'),
			]
		)
		self.fire_department_field.update_menu_items([f'Item #{i}' for i in range(10)])
		self.add_content(self.fire_department_field)

		self.add_content(MDBoxLayout())
