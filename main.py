# -*- coding: utf-8 -*-

# from kivy.uix.screenmanager import ScreenManager

# import config as Config
import db_models as DataBase


def main():
	DataBase.db.create_all()


if __name__ == '__main__':
	main()