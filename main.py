# -*- coding: utf-8 -*-

import db_models as DataBase
import config as Config
from UI import FireDepartment


def main():
	DataBase.db.create_all()
	FireDepartment().run()


if __name__ == '__main__':
	main()