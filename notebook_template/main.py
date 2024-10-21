# -*- coding: utf-8 -*-

from kivy.config import Config
Config.set('graphics', 'width', '360')
Config.set('graphics', 'height', '650')


# from data_base import db
from app import Application


def main() -> None:
	# db.create_all()

	app = Application()
	app.run()


if __name__ == '__main__':
	main()