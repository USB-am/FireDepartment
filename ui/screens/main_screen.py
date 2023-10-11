from app.path_manager import PathManager
from data_base import Emergency
from ui.screens.base_screen import BaseScreen
from ui.widgets.list_element import MainScreenElement
from ui.fields.switch import FDIconSwitch
from kivymd.uix.button import MDFlatButton


class MainScreen(BaseScreen):
	""" Главная страница """

	name = 'main'
	toolbar_title = 'Главная'

	def __init__(self, path_manager: PathManager):
		super().__init__(path_manager)

		self.ids.toolbar.add_left_button(icon='menu', callback=self.open_menu)

	def display(self) -> None:
		w1 = FDIconSwitch(
			icon='theme-light-dark',
			title='Theme',
			active_icon='white-balance-sunny',
			deactive_icon='weather-night'
		)
		self.add_content(w1)
		w1.set_value(True)

		b = MDFlatButton(text='Test')
		b.bind(on_release=lambda *e: print(w1.get_value()))
		self.add_content(b)