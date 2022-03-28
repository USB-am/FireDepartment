# -*- coding: utf-8 -*-

from db_models import db as DataBase
import config as Config
from UI import FireDepartment


def main():
	DataBase.create_all()
	FireDepartment().run()

2
if __name__ == '__main__':
	main()