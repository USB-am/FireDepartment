# -*- coding: utf-8 -*-

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

import config as Config


app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = Config.PATH_TO_DATA_BASE

db = SQLAlchemy(app)


post_tags = db.Table('post_tags',
	db.Column('tag_id', db.Integer, db.ForeignKey('Tag.id')),
	db.Column('post_id', db.Integer, db.ForeignKey('Post.id')),
)
post_persons = db.Table('post_persons',
	db.Column('person_id', db.Integer, db.ForeignKey('Person.id')),
	db.Column('post_id', db.Integer, db.ForeignKey('Post.id')),
)


class Tag(db.Model):
	__tablename__ = 'Tag'
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(255), unique=True, nullable=False)

	def __str__(self):
		return f'{self.id}. {self.title}'

	@staticmethod
	def get_fields() -> dict:
		result = {
			'title': 'StringField',
		}

		return result


class Rank(db.Model):
	__tablename__ = 'Rank'
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(255), unique=True, nullable=False)

	def __str__(self):
		return f'{self.id}. {self.title}'

	@staticmethod
	def get_fields() -> dict:
		result = {
			'title': 'StringField',
		}

		return result


class Position(db.Model):
	__tablename__ = 'Position'
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(255), unique=True, nullable=False)

	def __str__(self):
		return f'{self.id}. {self.title}'

	@staticmethod
	def get_fields() -> dict:
		result = {
			'title': 'StringField',
		}

		return result


class Person(db.Model):
	__tablename__ = 'Person'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(255), nullable=False)
	phone = db.Column(db.String(255), nullable=False)
	add_phone = db.Column(db.String(255), nullable=True)
	work_day = db.Column(db.DateTime(), nullable=True)
	work_type = db.Column(db.Integer, nullable=True)
	position = db.Column(db.Integer, db.ForeignKey('Position.id'), nullable=True)
	rank = db.Column(db.Integer, db.ForeignKey('Rank.id'), nullable=True)

	def __str__(self):
		return f'{self.id}. {self.name} - {self.phone}'

	@staticmethod
	def get_fields() -> dict:
		result = {
			'name': 'StringField',
			'phone': 'PhoneField',
			'add_phone': 'PhoneField',
			'work_day': 'CalendarField',
			'work_type': 'RadioField',
			'position': 'ForeignKeyField',
			'rank': 'ForeignKeyField',
		}

		return result


class Post(db.Model):
	__tablename__ = 'Post'
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(255), nullable=False)
	description = db.Column(db.Text(), nullable=True)
	tags = db.relationship('Tag', secondary=post_tags, backref='posts')
	persons = db.relationship('Person', secondary=post_persons, backref='posts')

	def __str__(self):
		return f'{self.id}. {self.title}'

	@staticmethod
	def get_fields() -> dict:
		result = {
			'title': 'StringField',
			'description': 'TextField',
			'persons': 'ForeignKeyField',
			'tags': 'ForeignKeyField',
		}

		return result