# -*- coding: utf-8 -*-

# from kivy.uix.screenmanager import ScreenManager

# import config as Config
import db_models as DataBase
from UI import FireDepartment


def main():
	DataBase.db.create_all()
	FireDepartment().run()


if __name__ == '__main__':
	main()