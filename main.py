# -*- coding: utf-8 -*-

from db_models import db as DataBase
DataBase.create_all()

from UI.fire_department import FireDepartment


def main():
	FireDepartment().run()


if __name__ == '__main__':
	main()