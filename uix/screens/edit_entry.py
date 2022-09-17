from kivymd.theming import ThemeManager

from config import LOCALIZED
from data_base import db
from uix import fields
from .create_entry import CreateEntryTag, CreateEntryRank, CreateEntryPosition, \
	CreateEntryHuman, CreateEntryEmergency, CreateEntryWorktype
from custom_screen import CustomScrolledScreen


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
		self.element.title = self.title.get_value()
		self.element.emergencys = self.emergencies.get_value()

		db.session.commit()

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
		self.element.title = self.title.get_value()

		db.session.commit()

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
		self.element.title = self.title.get_value()

		db.session.commit()

		self.path_manager.back()


class EditEntryHuman(CreateEntryHuman):
	''' Экран редаектирования человека '''

	def __init__(self, path_manager):
		super().__init__(path_manager)
		
		self.name = 'edit_human'
		self.toolbar.title = LOCALIZED.translate(self.name)
		self.element = None

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
		self.element.title = self.title.get_value()
		self.element.phone_1 = self.phone_1.get_value()
		self.element.phone_2 = self.phone_2.get_value()
		self.element.work_day = self.work_day.get_value()
		self.element.worktype = get_id_from_list(self.work_type)
		self.element.rank = get_id_from_list(self.rank)
		self.element.position = get_id_from_list(self.position)

		db.session.commit()

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
		self.element.title = self.title.get_value()
		self.element.description = self.description.get_value()
		self.element.urgent = self.urgent.get_value()
		self.element.humans = self.humans.get_value()
		self.element.tags = self.tags.get_value()

		db.session.commit()

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
		pass


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
			'arrow-left', lambda e: self.path_manager.back())

		colors_dict = ThemeManager().colors.copy()
		colors_dict.pop('Light', None)
		colors_dict.pop('Dark',  None)

		hue_items = fields.gen_hue_items(colors_dict['Red'].keys(), self.update_theme)
		color_items = fields.gen_color_items(colors_dict.keys(), self.update_theme)

		self.primary_hue = fields.DropDown(
			icon='opacity',
			title='Primary hue')
		self.primary_hue.add(hue_items)
		self.primary_palette = fields.DropDown(
			icon='palette',
			title='Primary palette')
		self.primary_palette.add(color_items)
		self.accent_palette = fields.DropDown(
			icon='exclamation-thick',
			title='Accent palette')
		self.accent_palette.add(color_items)
		self.theme_style = fields.BooleanField(
			icon='theme-light-dark',
			title='Theme')
		self.background_image = 'FileManagerField'

		self.add_widgets(self.primary_hue)
		self.add_widgets(self.primary_palette)
		self.add_widgets(self.accent_palette)
		self.add_widgets(self.theme_style)

	def fill_content(self) -> None:
		# self.primary_hue.set_value()
		pass

	def update_theme(self, value: str) -> None:
		print(value)