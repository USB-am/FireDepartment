from os import getcwd
from os.path import join as pjoin


__BASE_DIR = getcwd()
__STATIC_DIR = pjoin(__BASE_DIR, 'static')
__KV_DIR = pjoin(__BASE_DIR, 'kv')

# Screens
__SCREENS_DIR = pjoin(__KV_DIR, 'screens')
# __BASE_SCREEN_DIR = pjoin(__KV_DIR, 'base_screen.kv')

# Fields
__FIELDS_DIR = pjoin(__KV_DIR, 'fields')
__FIELD_INPUT_DIR = pjoin(__FIELDS_DIR, 'input.kv')
__FIELD_SELECT = pjoin(__FIELDS_DIR, 'select.kv')
__FIELD_SWITCH = pjoin(__FIELDS_DIR, 'switch.kv')
__FIELD_BUTTON = pjoin(__FIELDS_DIR, 'button.kv')
__FIELD_DROPDOWN = pjoin(__FIELDS_DIR, 'dropdown.kv')

# Widgets
__WIDGETS_DIR = pjoin(__KV_DIR, 'widgets')
__TOOLBAR_DIR = pjoin(__WIDGETS_DIR, 'toolbar.kv')