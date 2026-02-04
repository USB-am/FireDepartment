import os
import configparser


PATH_TO_SERVER = 'http://localhost:8000/'


ICONS = {
	'Tag': 'pound',
	'Short': 'text-short',
	'Rank': 'chevron-triple-up',
	'Position': 'crosshairs-gps',
	'Human': 'account-group',
	'Emergency': 'fire-alert',
	'ColorTheme': 'palette',
	'Worktype': 'timer-sand',
	'UserSettings': 'account-wrench',
	'Calls': 'firebase',

	'urgent': (
		'fire',
		'fire-alert',
	),
}


BASE_DIR = os.getcwd()


settings = configparser.ConfigParser()
settings.read(os.path.join(BASE_DIR, 'app', 'application.ini'))
try:
	ITERABLE_COUNT = int(settings.get('global', 'iterable_count'))
except (configparser.NoSectionError, ValueError):
	ITERABLE_COUNT = 10


# Path to secret_key
SECRET_KEY_PATH = os.path.join(BASE_DIR, 'service', 'server', 'secret_key.json')


# Paths to .kv files
KV_DIR = os.path.join(BASE_DIR, 'kv')


# Static
STATIC_DIR = os.path.join(BASE_DIR, 'static')

# Icons
ICONS_DIR = os.path.join(STATIC_DIR, 'icons')
APP_ICON = os.path.join(ICONS_DIR, 'icon.png')

# Images
IMAGES_DIR = os.path.join(STATIC_DIR, 'images')
LOGO_IMG = os.path.join(IMAGES_DIR, 'logo.png')

# Fonts
FONTS_DIR = os.path.join(STATIC_DIR, 'fonts')
NUMBER_FONT = os.path.join(FONTS_DIR, 'NumbersFont.ttf')

# Config
APP_DIR = os.path.join(BASE_DIR, 'app')
CONF = os.path.join(APP_DIR, 'application.ini')

# Screens
SCREENS_KV = os.path.join(KV_DIR, 'screens')
APP_SCREEN = os.path.join(SCREENS_KV, 'app_screen.kv')
BASE_SCREEN = os.path.join(SCREENS_KV, 'base_screen.kv')

# Widgets
WIDGETS_DIR = os.path.join(KV_DIR, 'widgets')
# NOTEBOOK_WIDGET = os.path.join(WIDGETS_DIR, 'notebook.kv')
# TRIPLE_CHECKBOX = os.path.join(WIDGETS_DIR, 'triple_checkbox.kv')
SEARCH_WIDGET = os.path.join(WIDGETS_DIR, 'search.kv')
NOTEBOOK_WIDGET = os.path.join(WIDGETS_DIR, 'notebook.kv')
NAVIGATION_WIDGET = os.path.join(WIDGETS_DIR, 'navigation.kv')

# Layouts
LAYOUTS_DIR = os.path.join(KV_DIR, 'layouts')
MAIN_SCREEN_LAYOUTS = os.path.join(LAYOUTS_DIR, 'main_screen.kv')
MODEL_LIST_LAYOUTS = os.path.join(LAYOUTS_DIR, 'model_list.kv')
DIALOG_LAYOUTS = os.path.join(LAYOUTS_DIR, 'dialogs.kv')
SELECT_LAYOUTS = os.path.join(LAYOUTS_DIR, 'select.kv')
LABEL_LAYOUT = os.path.join(LAYOUTS_DIR, 'label_layout.kv')
HISTORY_LAYOUT = os.path.join(LAYOUTS_DIR, 'history_layout.kv')

# Fields
FIELDS_DIR = os.path.join(KV_DIR, 'fields')
LABEL_FIELD = os.path.join(FIELDS_DIR, 'label.kv')
BUTTON_FIELD = os.path.join(FIELDS_DIR, 'button.kv')
INPUT_FIELD = os.path.join(FIELDS_DIR, 'input.kv')
SELECT_FIELD = os.path.join(FIELDS_DIR, 'select.kv')
SWITCH_FIELD = os.path.join(FIELDS_DIR, 'switch.kv')
CALENDAR_FIELD = os.path.join(FIELDS_DIR, 'calendar.kv')
CALL_HUMAN_FIELD_KV = os.path.join(FIELDS_DIR, 'call_human.kv')
