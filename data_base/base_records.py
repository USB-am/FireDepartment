from . import db, ColorTheme


def insert_colortheme() -> None:
	db_entry = ColorTheme.query.first()

	if db_entry is not None:
		return

	base_theme = ColorTheme(
		primary_palette='Blue',
		accent_palette='Amber',
		primary_hue='500',
		theme_style='Light',
		background_image=None
	)
	db.session.add(base_theme)
	db.session.commit()


def write_records():
	print('write_records is started!')
	insert_colortheme()
	print('write_records is finished!')