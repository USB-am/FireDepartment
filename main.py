# -*- coding: utf-8 -*-

from kivy.config import Config
Config.set('graphics', 'width', '360')
Config.set('graphics', 'height', '650')


from data_base import db, base_records
from app import Application


if __name__ == '__main__':
	db.create_all()
	base_records.write_records()

	app = Application()
	app.run()