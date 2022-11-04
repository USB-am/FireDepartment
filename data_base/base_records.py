from . import db, ColorTheme, UserSettings


def insert_colortheme() -> None:
	db_entry = ColorTheme.query.first()

	if db_entry is not None:
		return

	base_theme = ColorTheme(
		primary_palette='Blue',
		accent_palette='Amber',
		primary_hue='500',
		theme_style='Light',
		background_image=None,
		background_color='[1, 1, 1, 1]',
	)
	db.session.add(base_theme)
	db.session.commit()


def insert_usersettings() -> None:
	db_entry = UserSettings.query.first()

	if db_entry is not None:
		return

	base_settings = UserSettings(
		help_mode=True,
		language='ru',
	)
	db.session.add(base_settings)
	db.session.commit()


def write_records():
	insert_colortheme()
	insert_usersettings()