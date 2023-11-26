import os


BASE_DIR = os.getcwd()

KV_DIR = os.path.join(BASE_DIR, 'kv')

# Screens
SCREENS_KV = os.path.join(KV_DIR, 'screens')
APP_SCREEN = os.path.join(SCREENS_KV, 'app_screen.kv')
BASE_SCREEN = os.path.join(SCREENS_KV, 'base_screen.kv')

# Widgets
WIDGETS_DIR = os.path.join(KV_DIR, 'widgets')
NOTEBOOK_WIDGET = os.path.join(WIDGETS_DIR, 'notebook.kv')
TRIPLE_CHECKBOX = os.path.join(WIDGETS_DIR, 'triple_checkbox.kv')