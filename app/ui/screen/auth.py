from kivy.lang.builder import Builder
from kivy.metrics import dp
from kivymd.uix.boxlayout import MDBoxLayout

from path_manager import PathManager
from .based_screen import BaseScreen
from ui.widgets.label import FDLabel
from ui.widgets.text_input import FDTextInput, FDPasswordInput
from ui.widgets.button import FDRectangleFillButton
from validators.widgets import EmptyValidator


class FDAuthScreen(BaseScreen):
	name = 'auth'
	title = 'Авторизация'

	def __init__(self, path_manager: PathManager):
		super().__init__(path_manager)
		self.ids.toolbar.anchor_title = 'center'

	def on_kv_post(self, instance: 'FDAuthScreen') -> None:
		auth_label = FDLabel(text='Авторизироваться', font_style='H5')
		self.add_content(auth_label)

		self.login_field = FDTextInput(
			hint_text='Логин',
			validators=[
				EmptyValidator(error_msg='Поле не может быть пустым!')
			]
		)
		self.add_content(self.login_field)

		self.password_field = FDPasswordInput(
			hint_text='Пароль',
			validators=[
				EmptyValidator(error_msg='Поле не может быть пустым!')
			]
		)
		self.add_content(self.password_field)

		self.auth_btn = FDRectangleFillButton(
			text='Войти'
		)
		self.add_content(self.auth_btn)

		self.add_content(MDBoxLayout(size_hint=(1, None), height=dp(4)))

		self.register_btn = FDRectangleFillButton(
			text='Регистрация'
		)
		self.register_btn.bind(on_release=lambda *_: self.path_manager.forward('register'))
		self.add_content(self.register_btn)

		self.add_content(MDBoxLayout())
