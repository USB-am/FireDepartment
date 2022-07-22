# -*- coding: utf-8 -*-

from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager

from app.screens import MainPage
from config.path_manager import PathManager


class Application(MDApp):
	def __init__(self):
		super().__init__()

		self.path_manager = PathManager()
		self.screen_manager = ScreenManager()

		# Main page
		self.screen_manager.add_widget(MainPage())

		self.screen_manager.current = 'main_page'

	def back(self) -> None:
		self.path_manager.back()
		self.screen_manager.current = self.path_manager.current

	def forward(self, screen_name: str) -> None:
		self.path_manager.forward(screen_name)
		self.screen_manager.current = self.path_manager.current

	def build(self) -> ScreenManager:
		return self.screen_manager


def main():
	app = Application()
	app.run()


if __name__ == '__main__':
	main()