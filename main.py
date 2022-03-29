# -*- coding: utf-8 -*-

from db_models import db as DataBase
import config as Config
from UI import FireDepartment
from UI.exceptions import global_exception


@global_exception
def main():
	DataBase.create_all()
	FireDepartment().run()


if __name__ == '__main__':
	main()