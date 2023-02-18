# -*- coding: utf-8 -*-

from kivy.config import Config
Config.set('graphics', 'width', '360')
Config.set('graphics', 'height', '650')


from app import Application


if __name__ == '__main__':
	app = Application()
	app.run()