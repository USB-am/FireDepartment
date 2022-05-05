# -*- coding: utf-8 -*-

from data_base import db as DataBase
DataBase.create_all()


from app import Application

if __name__ == '__main__':
	Application().run()