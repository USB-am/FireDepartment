# -*- coding: utf-8 -*-

# Temp import
from kivy.config import Config
# Config.set("graphics", "resizable", "0")
Config.set('graphics', 'width', '350')


from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager

from app.screens import \
	MainPage, \
	Fires, \
	Options, \
	TagEditList, RankEditList, PositionEditList, HumanEditList, EmergencyEditList, \
	EditTag, EditRank, EditPosition, EditHuman, EditEmergency, \
	CreateTag, CreateRank, CreatePosition, CreateHuman, CreateEmergency
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

		# Fires page
		self.screen_manager.add_widget(Fires())

		# Options page
		self.screen_manager.add_widget(Options())

		# Create page
		self.screen_manager.add_widget(CreateTag())
		self.screen_manager.add_widget(CreateRank())
		self.screen_manager.add_widget(CreatePosition())
		self.screen_manager.add_widget(CreateHuman())
		self.screen_manager.add_widget(CreateEmergency())

		# Edit list page
		self.screen_manager.add_widget(TagEditList())
		self.screen_manager.add_widget(RankEditList())
		self.screen_manager.add_widget(PositionEditList())
		self.screen_manager.add_widget(HumanEditList())
		self.screen_manager.add_widget(EmergencyEditList())

		# Edit page
		self.screen_manager.add_widget(EditTag())
		self.screen_manager.add_widget(EditRank())
		self.screen_manager.add_widget(EditPosition())
		self.screen_manager.add_widget(EditHuman())
		self.screen_manager.add_widget(EditEmergency())

		self.screen_manager.current = 'edit_human_list'

	def build(self) -> ScreenManager:
		return self.screen_manager


def main():
	app = Application()
	app.run()


if __name__ == '__main__':
	main()