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
	# post = db.relationship('Post', backref='tag')

	def __str__(self):
		return f'{self.id}. {self.title}'


class Rank(db.Model):
	__tablename__ = 'Rank'
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(255), unique=True, nullable=False)
	# person = db.relationship('Person', backref='rank', uselist=False)

	def __str__(self):
		return f'{self.id}. {self.title}'


class Position(db.Model):
	__tablename__ = 'Position'
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(255), unique=True, nullable=False)
	# person = db.relationship('Person', backref='position', uselist=False)

	def __str__(self):
		return f'{self.id}. {self.title}'


class Person(db.Model):
	__tablename__ = 'Person'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(255), nullable=False)
	phone = db.Column(db.String(255), nullable=False)
	add_phone = db.Column(db.String(255), nullable=True)
	work_day = db.Column(db.DateTime(), nullable=True)
	work_time = db.Column(db.Time(), nullable=True)
	day_off_time = db.Column(db.Time(), nullable=True)
	position = db.Column(db.Integer, db.ForeignKey('Position.id'), nullable=True)
	rank = db.Column(db.Integer, db.ForeignKey('Rank.id'), nullable=True)

	def __str__(self):
		return f'{self.id}. {self.name} - {self.phone}'


class Post(db.Model):
	__tablename__ = 'Post'
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(255), nullable=False)
	tags = db.relationship('Tag', secondary=post_tags, backref='posts')
	persons = db.relationship('Person', secondary=post_persons, backref='posts')

	def __str__(self):
		return f'{self.id}. {self.title}'