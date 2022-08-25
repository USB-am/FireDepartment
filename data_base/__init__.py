# -*- coding: utf-8 -*-

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# from uix import fields


app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///fire_department.db'


db = SQLAlchemy(app)


post_tags = db.Table('emergency_tags',
	db.Column('tag_id', db.Integer, db.ForeignKey('Tag.id')),
	db.Column('emergency_id', db.Integer, db.ForeignKey('Emergency.id')),
)
post_humans = db.Table('emergency_humans',
	db.Column('human_id', db.Integer, db.ForeignKey('Human.id')),
	db.Column('emergency_id', db.Integer, db.ForeignKey('Emergency.id')),
)


class Tag(db.Model):
	icon = 'pound'
	__tablename__ = 'Tag'
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(255), unique=True, nullable=False)

	def __str__(self):
		return self.title

	@staticmethod
	def get_fields() -> dict:
		return {
			'title': 'fields.StringField',
			'emergencys': 'ManyToManyField'
		}


class Rank(db.Model):
	icon = 'chevron-triple-up'
	__tablename__ = 'Rank'
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(255), unique=True, nullable=False)

	def __str__(self):
		return self.title

	@staticmethod
	def get_fields() -> dict:
		return {
			'title': 'fields.StringField',
		}


class Position(db.Model):
	icon = 'crosshairs-gps'
	__tablename__ = 'Position'
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(255), unique=True, nullable=False)

	def __str__(self):
		return self.title

	@staticmethod
	def get_fields() -> dict:
		return {
			'title': 'fields.StringField',
		}


class Human(db.Model):
	icon = 'account-group'
	__tablename__ = 'Human'
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(255), nullable=False)
	phone_1 = db.Column(db.String(255), nullable=True)
	phone_2 = db.Column(db.String(255), nullable=True)
	work_day = db.Column(db.DateTime(), nullable=True)
	worktype = db.Column(db.Integer, db.ForeignKey('Worktype.id'), nullable=True)
	position = db.Column(db.Integer, db.ForeignKey('Position.id'), nullable=True)
	rank = db.Column(db.Integer, db.ForeignKey('Rank.id'), nullable=True)

	def __str__(self):
		return self.title

	@staticmethod
	def get_fields() -> dict:
		return {
			'title': 'fields.StringField',
			'phone_1': 'fields.PhoneField',
			'phone_2': 'fields.PhoneField',
			'work_day': 'WorkDayField',
			'worktype': 'ForeignKeyField',
			'position': 'ForeignKeyField',
			'rank': 'ForeignKeyField',
		}


class Emergency(db.Model):
	icon = 'fire-alert'
	__tablename__ = 'Emergency'
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(255), nullable=False)
	description = db.Column(db.Text(), nullable=True)
	urgent = db.Column(db.Boolean(), nullable=True)
	tags = db.relationship('Tag', secondary=post_tags, backref='emergencys')
	humans = db.relationship('Human', secondary=post_humans, backref='emergencys')

	def __str__(self):
		return self.title

	@staticmethod
	def get_fields() -> dict:
		return {
			'title': 'fields.StringField',
			'description': 'fields.DescriptionField',
			'urgent': 'fields.BooleanField',
			'humans': 'ManyToManyField',
			'tags': 'ManyToManyField',
		}


class ColorTheme(db.Model):
	icon = 'palette'
	__tablename__ = 'ColorTheme'
	id = db.Column(db.Integer, primary_key=True)
	primary_palette = db.Column(db.String(255), nullable=False)
	accent_palette = db.Column(db.String(255), nullable=False)
	primary_hue = db.Column(db.String(255), nullable=False)	# Оттенок
	theme_style = db.Column(db.String(255), nullable=False)	# Light/Dark
	background_image = db.Column(db.Text(), nullable=True)

	def __str__(self):
		return f'<ColorTheme {self.id}>'

	@staticmethod
	def get_fields() -> dict:
		result = {
			'primary_hue': 'SelectField',
			'primary_palette': 'SelectField',
			'accent_palette': 'SelectField',
			'theme_style': 'StyleRadioField',
			'background_image': 'FileManagerField'
		}

		return result


class Worktype(db.Model):
	icon = 'timer-sand'
	__tablename__ = 'Worktype'
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(255), nullable=False)
	start_work_day = db.Column(db.DateTime(), nullable=False)
	finish_work_day = db.Column(db.DateTime(), nullable=False)
	work_day_range = db.Column(db.Integer, nullable=False)
	week_day_range = db.Column(db.Integer, nullable=False)

	def __str__(self):
		return self.title

	def get_fields() -> dict:
		result = {
			'title': 'StringField',
			'start_work_day': 'DateTimeField',
			'finish_work_day': 'DateTimeField',
			'work_day_range': 'fields.IntegerField',
			'week_day_range': 'fields.IntegerField',
		}

		return result