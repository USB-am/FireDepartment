import os


BASE_DIR = os.getcwd()

KV_DIR = os.path.join(BASE_DIR, 'kv')
KV_WIDGETS_DIR = os.path.join(KV_DIR, 'widgets')

APP_KV = os.path.join(KV_DIR, 'app.kv')
SCREENS_KV = os.path.join(KV_DIR, 'screens')

HOME_KV = os.path.join(SCREENS_KV, 'home.kv')

# Widgets
NOTEBOOK_WIDGET_KV = os.path.join(KV_WIDGETS_DIR, 'notebook.kv')
NAVIGATION_WIDGET_KV = os.path.join(KV_WIDGETS_DIR, 'navigation.kv')
