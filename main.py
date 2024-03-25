# -*- coding: utf-8 -*-

from kivy.config import Config
Config.set('graphics', 'width', '360')
Config.set('graphics', 'height', '650')


from data_base import db
from app import Application

from call_manager import test


def main() -> None:
	db.create_all()

	app = Application()
	test()
	app.run()



if __name__ == '__main__':
	main()