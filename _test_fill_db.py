# -*- coding: utf-8 -*-

from db_models import db, Tag, Rank, Position, Person, Post


try:
	base_models = (Tag, Rank, Position)

	for table in base_models:
		db.session.add_all([table(
			title='{name} #{num}'.format(name=table.__tablename__, num=i+1),
		) for i in range(10)])


	db.session.add_all([Person(
		name='{name} #{num}'.format(name=table.__tablename__, num=i+1),
		phone=f'8800555353{i}'
	) for i in range(10)])

	db.session.add_all([Post(
		title='{name} #{num}'.format(name=table.__tablename__, num=i+1),
		urgent=False
	) for i in range(10)])

	db.session.commit()
except Exception as e:
	print(e)
	db.session.rollback()