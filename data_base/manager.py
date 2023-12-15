from typing import Any, Dict, Type

from data_base import db, Tag, Rank, Position, Human, Emergency, Worktype


def write_entry(model: Type[db.Model], params: Dict[str, Any]) -> db.Model:
	'''
	Создать запись в БД.

	~params:
	model: Type[db.Model] - модель, в которую будет произведена запись;
	params: Dict[str, Any] - словарь с данными о записи.
	'''

	entry = model(**params)

	db.session.add(entry)
	# db.session.commit()

	return entry
