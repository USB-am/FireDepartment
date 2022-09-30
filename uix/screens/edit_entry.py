from kivymd.theming import ThemeManager

from config import LOCALIZED
from data_base import db, ColorTheme
from data_base import manager as DBManager
from uix import fields
from .create_entry import CreateEntryTag, CreateEntryRank, CreateEntryPosition, \
	CreateEntryHuman, CreateEntryEmergency, CreateEntryWorktype
from custom_screen import CustomScreen, CustomScrolledScreen


from random import random, randint


def get_id_from_list(foreign_key_field: fields.SelectedList) -> int:
	selected_element = foreign_key_field.get_value()

	return selected_element[0].id if selected_element else None


class EditEntryTag(CreateEntryTag):
	''' Экран редаектирования тега '''

	def __init__(self, path_manager):
		super().__init__(path_manager)

		self.name = 'edit_tag'
		self.toolbar.title = LOCALIZED.translate(self.name)
		self.element = None

	def set_element(self, element: db.Model) -> None:
		self.element = element

		self.fill_fields()

	def fill_fields(self) -> None:
		self.title.set_value(self.element.title)
		self.emergencies.set_value(self.element.emergencys)

	def insert(self) -> None:
		values = {
			'title': self.title.get_value(),
			'emergencys': self.emergencies.get_value()}

		successful_entry = DBManager.update(self.element, values)

		if successful_entry:
			self.path_manager.back()


class EditEntryRank(CreateEntryRank):
	''' Экран редаектирования звания '''

	def __init__(self, path_manager):
		super().__init__(path_manager)

		self.name = 'edit_rank'
		self.toolbar.title = LOCALIZED.translate(self.name)
		self.element = None

	def set_element(self, element: db.Model) -> None:
		self.element = element

		self.fill_fields()

	def fill_fields(self) -> None:
		self.title.set_value(self.element.title)

	def insert(self) -> None:
		values = {'tite': self.title.get_value()}
		successful_entry = DBManager.update(self.element, values)

		if successful_entry:
			self.path_manager.back()


class EditEntryPosition(CreateEntryPosition):
	''' Экран редаектирования должности '''

	def __init__(self, path_manager):
		super().__init__(path_manager)

		self.name = 'edit_position'
		self.toolbar.title = LOCALIZED.translate(self.name)
		self.element = None

	def set_element(self, element: db.Model) -> None:
		self.element = element

		self.fill_fields()

	def fill_fields(self) -> None:
		self.title.set_value(self.element.title)

	def insert(self) -> None:
		values = {'tite': self.title.get_value()}
		successful_entry = DBManager.update(self.element, values)

		if successful_entry:
			self.path_manager.back()


class EditEntryHuman(CreateEntryHuman):
	''' Экран редаектирования человека '''

	def __init__(self, path_manager):
		super().__init__(path_manager)
		
		self.name = 'edit_human'
		self.toolbar.title = LOCALIZED.translate(self.name)
		self.element = None

		# self.bind(on_pre_enter=lambda e: super().update_selected_lists())

	def set_element(self, element: db.Model) -> None:
		self.element = element

		self.fill_fields()

	def fill_fields(self) -> None:
		self.title.set_value(self.element.title)
		self.phone_1.set_value(self.element.phone_1)
		self.phone_2.set_value(self.element.phone_2)
		self.work_day.set_value(self.element.work_day)
		self.rank.set_value(self.element.rank)
		self.position.set_value(self.element.position)

	def insert(self) -> None:
		values = {
			'tite': self.title.get_value(),
			'phone_1': self.phone_1.get_value(),
			'phone_2': self.phone_2.get_value(),
			'work_day': self.work_day.get_value(),
			'worktype': get_id_from_list(self.work_type),
			'rank': get_id_from_list(self.rank),
			'position': get_id_from_list(self.position)
		}

		successful_entry = DBManager.update(self.element, values)

		if successful_entry:
			self.path_manager.back()


class EditEntryEmergency(CreateEntryEmergency):
	''' Экран редаектирования ЧС '''

	def __init__(self, path_manager):
		super().__init__(path_manager)
		
		self.name = 'edit_emergency'
		self.toolbar.title = LOCALIZED.translate(self.name)
		self.element = None

	def set_element(self, element: db.Model) -> None:
		self.element = element

		self.fill_fields()

	def fill_fields(self) -> None:
		self.title.set_value(self.element.title)
		self.description.set_value(self.element.description)
		self.urgent.set_value(self.element.urgent)
		self.humans.set_value(self.element.humans)
		self.tags.set_value(self.element.tags)

	def insert(self) -> None:
		values = {
			'title': self.title.get_value(),
			'description': self.description.get_value(),
			'urgent': self.urgent.get_value(),
			'humans': self.humans.get_value(),
			'tags': self.tags.get_value()
		}

		successful_entry = DBManager.update(self.element, values)

		if successful_entry:
			self.path_manager.back()


class EditEntryWorktype(CreateEntryWorktype):
	''' Экран редаектирования графика работы '''

	def __init__(self, path_manager):
		super().__init__(path_manager)
		
		self.name = 'edit_worktype'
		self.toolbar.title = LOCALIZED.translate(self.name)
		self.element = None

	def set_element(self, element: db.Model) -> None:
		self.element = element

		self.fill_fields()

	def fill_fields(self) -> None:
		self.title.set_value(self.element.title)
		self.start_work_day.set_value(self.element.start_work_day)
		self.finish_work_day.set_value(self.element.finish_work_day)
		self.work_day_range.set_value(self.element.work_day_range)
		self.week_day_range.set_value(self.element.week_day_range)

	def insert(self) -> None:
		values = {
			'title': self.title.get_value(),
			'start_work_day': self.start_work_day.get_value(),
			'finish_work_day': self.finish_work_day.get_value(),
			'work_day_range': self.work_day_range.get_value(),
			'week_day_range': self.week_day_range.get_value()
		}

		successful_entry = DBManager.update(self.element, values)

		if successful_entry:
			self.path_manager.back()


class EditColorTheme(CustomScrolledScreen):
	''' Экран редактирования цветной схемы '''

	def __init__(self, path_manager, theme_cls):
		super().__init__()

		self.path_manager = path_manager
		self.theme_cls = theme_cls
		self.theme_cls.theme_style_switch_animation = True
		self.theme_cls.theme_style_switch_animation_duration = .3

		self.name = 'edit_colortheme'

		self.setup()
		self.fill_content()

	def setup(self) -> None:
		self.toolbar.title = LOCALIZED.translate(self.name)
		self.toolbar.add_left_button(
			'arrow-left', lambda e: self.save_changes_and_back())

		colors_dict = ThemeManager().colors.copy()
		colors_dict.pop('Light', None)
		colors_dict.pop('Dark',  None)

		hue_items = fields.gen_hue_items(colors_dict['Red'].keys(), self.change_hue)
		primary_items = fields.gen_color_items(colors_dict.keys(), self.change_primary)
		accent_items = fields.gen_color_items(colors_dict.keys(), self.change_accent)

		# HUE
		self.primary_hue = fields.DropDown(icon='opacity',
		                                   title='Primary hue')
		self.primary_hue.add(hue_items)
		# PRIMARY
		self.primary_palette = fields.DropDown(icon='palette',
		                                       title='Primary palette')
		self.primary_palette.add(primary_items)
		# ACCENT
		self.accent_palette = fields.DropDown(icon='exclamation-thick',
		                                      title='Accent palette')
		self.accent_palette.add(accent_items)
		# THEME STYLE
		self.theme_style = fields.BooleanField(icon='theme-light-dark',
		                                       title='Dark theme')
		self.theme_style.ids.switch.bind(
			on_release=lambda e: self.change_theme_style())
		# BACKGROUND IMAGE
		self.background_image = fields.FileManager(
			title='Background image',
			path='\\',
			select_path=lambda e: self.exit_filemanager_and_change_background(e),
			preview=True)
		self.background_opacity = fields.FDSlider(icon='window-closed-variant',
		                                          title='Background opacity')
		#self.background_opacity.ids.slider.bind(on_touch_up=lambda *e: \
		#	self.change_opacity())

		self.add_widgets(self.primary_hue)
		self.add_widgets(self.primary_palette)
		self.add_widgets(self.accent_palette)
		self.add_widgets(self.theme_style)
		self.add_widgets(self.background_image)
		self.add_widgets(self.background_opacity)

	def save_changes(self) -> None:
		db_entry = ColorTheme.query.first()
		values = {
			'primary_palette': self.primary_palette.get_value(),
			'accent_palette': self.accent_palette.get_value(),
			'primary_hue': self.primary_hue.get_value(),
			'theme_style': 'Dark' if self.theme_style.get_value() else 'Light',
			'background_image': self.background_image.get_value(),
		}

		DBManager.update(db_entry, values)

	def save_changes_and_back(self) -> None:
		self.save_changes()
		self.path_manager.back()

	def update_bg_color(self) -> None:
		clr = (1, 1, 1, random())
		self.reboot_styles(rgba=clr)

	def change_theme_style(self) -> None:
		value = self.theme_style.get_value()
		if value:
			self.theme_cls.theme_style = 'Dark'
		else:
			self.theme_cls.theme_style = 'Light'

	def change_hue(self, value: str) -> None:
		self.theme_cls.primary_hue = value

	def change_primary(self, value: str):
		self.theme_cls.primary_palette = value

	def change_accent(self, value: str):
		self.theme_cls.accent_palette = value

	def exit_filemanager_and_change_background(self, path: str) -> None:
		self.close_filemanager()
		self.change_background(path)

	def close_filemanager(self) -> None:
		self.background_image.close_dialog()

	def change_background(self, path: str) -> None:
		self.reboot_styles(source=path)

	def fill_content(self) -> None:
		db_entry = ColorTheme.query.first()

		self.primary_hue.set_value(db_entry.primary_hue)
		self.primary_palette.set_value(db_entry.primary_palette)
		self.accent_palette.set_value(db_entry.accent_palette)
		self.theme_style.set_value(db_entry.theme_style == 'Dark')
		self.background_image.set_value(db_entry.background_image)
		# self.background_opacity.set_value()