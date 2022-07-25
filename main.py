# -*- coding: utf-8 -*-

# Temp import
from kivy.config import Config
# Config.set("graphics", "resizable", "0")
Config.set('graphics', 'width', '350')


from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager

from app.screens import MainPage, Fires
from config.path_manager import PathManager
from data_base import db


db.create_all()


class Application(MDApp):
	def __init__(self):
		super().__init__()

		self.screen_manager = ScreenManager()
		self.path_manager = PathManager(self.screen_manager)

		# Main page
		self.screen_manager.add_widget(MainPage())
		self.screen_manager.add_widget(Fires())

		self.screen_manager.current = 'main_page'

	def build(self) -> ScreenManager:
		return self.screen_manager


def main():
	app = Application()
	app.run()


if __name__ == '__main__':
	main()