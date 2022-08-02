from . import db


def insert(model: db.Model, values: dict) -> None:
	model_object = model(**values)

	db.session.add(model_object)
	db.session.commit()


def update(model: db.Model, values: dict) -> None:
	for column_name, value in values.items():
		setattr(model, column_name, value)

	db.session.commit()