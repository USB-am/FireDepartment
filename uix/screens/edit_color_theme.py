import json

from kivymd.theming import ThemeManager

from custom_screen import CustomScrolledScreen
from config import LOCALIZED, STATIC_DIR
from data_base import ColorTheme
from data_base import manager as DBManager
from uix import fields
from custom_screen import CustomScrolledScreen


class EditColorTheme(CustomScrolledScreen):
	''' Экран редактирования цветной схемы '''

	name = 'edit_colortheme'

	def __init__(self, path_manager, theme_cls):
		super().__init__()

		self.path_manager = path_manager
		self.theme_cls = theme_cls
		self.theme_cls.theme_style_switch_animation = True
		self.theme_cls.theme_style_switch_animation_duration = .3

		self.setup()
		self.fill_content()
		self.update_dropdown_fields()

	def setup(self) -> None:
		self.toolbar.title = LOCALIZED.translate(self.name)
		self.toolbar.add_left_button(
			'arrow-left', lambda e: self.save_changes_and_back())

		# HUE
		self.primary_hue = fields.DropDown(icon='opacity', title='Primary hue',
			help_text='Выбор оттенка цветовой темы')
		# PRIMARY
		self.primary_palette = fields.DropDown(icon='palette', title='Primary palette',
			help_text='Выбор основного цвета темы')
		# ACCENT
		self.accent_palette = fields.DropDown(icon='exclamation-thick', title='Accent palette',
			help_text='Выбор акцентирующего цвета')
		# THEME STYLE
		self.theme_style = fields.BooleanField(icon='theme-light-dark',
			title='Dark theme', help_text='Светлая/Темная тема')
		self.theme_style.ids.switch.bind(
			on_release=lambda e: self.change_theme_style())
		# BACKGROUND IMAGE
		self.background_image = fields.FileManager(
			title='Background image',
			path=STATIC_DIR,
			select_path=self.exit_filemanager_and_change_background,
			selector='file',
			preview=True,
			help_text='Выбор картинки заднего фона\n'
				'Если цвет фона - черный, картинка отображаться не будет!'
			)
		self.background_opacity = fields.FDSlider(
			icon='opacity',
			title=LOCALIZED.translate('Opacity'),
			help_text='Управление прозрачностью изображения заднего фона')
		self.background_opacity.ids.slider.bind(value=lambda instance, value: \
			self.update_bg_color_opacity())
		# BACKGROUND COLOR
		self.background_color = fields.FDColor(
			icon='format-color-fill',
			title='Background color',
			on_color=self.update_bg_color,
			help_text='Устанавливает цвет и прозрачность фона.\n\n'
				'Если установить черный цвет, не будет отображаться '
				'картинка заднего фона т.к. он влияет еще и на '
				'ее прозрачность!'
		)

		self.add_widgets(self.primary_hue)
		self.add_widgets(self.primary_palette)
		self.add_widgets(self.accent_palette)
		self.add_widgets(self.theme_style)
		self.add_widgets(self.background_image)
		self.add_widgets(self.background_opacity)
		self.add_widgets(self.background_color)

	def save_changes(self) -> None:
		bg_color = json.dumps(self.background_color.get_value())

		db_entry = ColorTheme.query.first()
		values = {
			'primary_palette': self.primary_palette.get_value(),
			'accent_palette': self.accent_palette.get_value(),
			'primary_hue': self.primary_hue.get_value(),
			'theme_style': 'Dark' if self.theme_style.get_value() else 'Light',
			'background_image': self.background_image.get_value(),
			'background_color': bg_color,
		}

		DBManager.update(db_entry, values)
		self.update_dropdown_fields()

	def save_changes_and_back(self) -> None:
		self.save_changes()
		self.path_manager.back()

	def update_bg_color(self, color: list) -> None:
		self.reboot_styles(rgba=color)
		self.save_changes()

	def update_bg_color_opacity(self) -> None:
		color = [*self.color[:-1], self.background_opacity.get_value()]
		self.reboot_styles(rgba=color)

		self.background_color.set_value(self.color)

	def change_theme_style(self) -> None:
		value = self.theme_style.get_value()
		if value:
			self.theme_cls.theme_style = 'Dark'
		else:
			self.theme_cls.theme_style = 'Light'

		self.save_changes()
		self.reboot_styles()

	def change_hue(self, value: str) -> None:
		self.theme_cls.primary_hue = value
		self.primary_hue.set_value(value)

		self.save_changes()

	def change_primary(self, value: str):
		self.theme_cls.primary_palette = value
		self.primary_palette.set_value(value)

		self.save_changes()

	def change_accent(self, value: str):
		self.theme_cls.accent_palette = value
		self.accent_palette.set_value(value)

		self.save_changes()

	def exit_filemanager_and_change_background(self, path: str) -> None:
		self.close_filemanager(path)
		self.change_background(path)

	def close_filemanager(self, path: str) -> None:
		self.background_image.close_dialog()
		self.background_image.set_value(path)

	def change_background(self, path: str) -> None:
		try:
			self.reboot_styles(source=path)
			self.background_image.set_value(path)
		except PermissionError:
			return

		self.save_changes()

	def fill_content(self) -> None:
		db_entry = ColorTheme.query.first()

		self.primary_hue.set_value(db_entry.primary_hue)
		self.primary_palette.set_value(db_entry.primary_palette)
		self.accent_palette.set_value(db_entry.accent_palette)
		self.theme_style.set_value(db_entry.theme_style == 'Dark')
		self.background_image.set_value(db_entry.background_image)
		bg_color_obj = json.loads(db_entry.background_color)
		self.background_color.set_value(bg_color_obj)

	def update_dropdown_fields(self) -> None:
		colors_dict = ThemeManager().colors.copy()
		colors_dict.pop('Light', None)
		colors_dict.pop('Dark',  None)

		hue_items = fields.gen_hue_items(
			colors_dict['Red'].keys(),
			self.change_hue)
		primary_items = fields.gen_color_items(
			colors_dict.keys(),
			self.change_primary)
		accent_items = fields.gen_color_items(
			colors_dict.keys(),
			self.change_accent)

		self.primary_hue.update_items(hue_items)
		self.primary_palette.update_items(primary_items)
		self.accent_palette.update_items(accent_items)