import os
import configparser


BASE_DIR = os.getcwd()


settings = configparser.ConfigParser()
settings.read(os.path.join(BASE_DIR, 'app', 'application.ini'))
try:
	ITERABLE_COUNT = int(settings.get('global', 'iterable_count'))
except (configparser.NoSectionError, ValueError):
	ITERABLE_COUNT = 10


# Paths to .kv files
KV_DIR = os.path.join(BASE_DIR, 'kv')


# Static
STATIC_DIR = os.path.join(BASE_DIR, 'static')
APP_ICON = os.path.join(STATIC_DIR, 'icon.png')
LOGO_IMG = os.path.join(STATIC_DIR, 'logo.png')

# Config
APP_DIR = os.path.join(BASE_DIR, 'app')
CONF = os.path.join(APP_DIR, 'application.ini')

# Screens
SCREENS_KV = os.path.join(KV_DIR, 'screens')
APP_SCREEN = os.path.join(SCREENS_KV, 'app_screen.kv')
BASE_SCREEN = os.path.join(SCREENS_KV, 'base_screen.kv')

# Widgets
WIDGETS_DIR = os.path.join(KV_DIR, 'widgets')
NOTEBOOK_WIDGET = os.path.join(WIDGETS_DIR, 'notebook.kv')
TRIPLE_CHECKBOX = os.path.join(WIDGETS_DIR, 'triple_checkbox.kv')
SEARCH_WIDGET = os.path.join(WIDGETS_DIR, 'search.kv')

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