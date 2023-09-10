# -*- coding: utf-8 -*-

# Delete this for prod
from kivy.config import Config
Config.set('graphics', 'width', '360')
Config.set('graphics', 'height', '650')


from data_base import db
from app import Application


if __name__ == '__main__':
	db.create_all()

	app = Application()
	app.run()