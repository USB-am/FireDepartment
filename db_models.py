# -*- coding: utf-8 -*-

import re

from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///fire_department.db'

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
		return self.title

	@staticmethod
	def get_fields() -> dict:
		result = {
			'title': 'StringField',
			'posts': 'ManyToManyField',
		}

		return result


class Rank(db.Model):
	__tablename__ = 'Rank'
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(255), unique=True, nullable=False)

	def __str__(self):
		return self.title

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
		return self.title

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
		return self.name

	def __get_show_phone(self) -> str:
		if self.phone is None:
			return ''

		return re.sub(
			FDPhoneTextInput._COMPLITE_PATTERN,
			FDPhoneTextInput._REPL,
			self.phone
		)

	@staticmethod
	def get_fields() -> dict:
		result = {
			'name': 'StringField',
			'phone': 'PhoneField',
			'add_phone': 'PhoneField',
			'work_type': 'WorkTypeField',
			'work_day': 'WorkDayField',
			'position': 'ForeignKeyField',
			'rank': 'ForeignKeyField',
			'posts': 'ManyToManyField',
		}

		return result


class Post(db.Model):
	__tablename__ = 'Post'
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(255), nullable=False)
	description = db.Column(db.Text(), nullable=True)
	urgent = db.Column(db.Boolean(), nullable=False)
	tags = db.relationship('Tag', secondary=post_tags, backref='posts')
	persons = db.relationship('Person', secondary=post_persons, backref='posts')

	def __str__(self):
		return self.title

	@staticmethod
	def get_fields() -> dict:
		result = {
			'title': 'StringField',
			'description': 'TextField',
			'urgent': 'BooleanField',
			'persons': 'ManyToManyField',
			'tags': 'ManyToManyField',
		}

		return result


class ColorTheme(db.Model):
	__tablename__ = 'ColorTheme'
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.PickleType, nullable=False)
	button_color = db.Column(db.PickleType, nullable=False)
	font_color = db.Column(db.PickleType, nullable=False)
	background_color_opacity = db.Column(db.PickleType, nullable=False)
	background_image = db.Column(db.String(255), nullable=False)

	def get_values(self) -> dict:
		return {
			'ID': self.id,
			'TITLE': self.title,
			'BUTTON_COLOR': self.button_color,
			'FONT_COLOR': self.font_color,
			'BACKGROUND_COLOR_OPACITY': self.background_color_opacity,
			'BACKGROUND_IMAGE': self.background_image
		}

	def __str__(self):
		return self.title