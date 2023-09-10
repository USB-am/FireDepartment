from os import getcwd
from os.path import join as pjoin


__BASE_DIR = getcwd()
__KV_DIR = pjoin(__BASE_DIR, 'kv')

# Screens
__SCREENS_DIR = pjoin(__KV_DIR, 'screens')
__BASE_SCREEN_DIR = pjoin(__KV_DIR, 'base_screen.kv')

# Widgets
__WIDGETS_DIR = pjoin(__KV_DIR, 'widgets')
__TOOLBAR_DIR = pjoin(__WIDGETS_DIR, 'toolbar.kv')