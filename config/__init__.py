import os

from .localized import Localized


# DIRS
BASE_DIR = os.getcwd()
STATIC_DIR = os.path.join(BASE_DIR, 'static')

KV_DIR = os.path.join(BASE_DIR, 'kv')
UIX_KV_DIR = os.path.join(KV_DIR, 'uix')
FIELDS_KV_DIR = os.path.join(UIX_KV_DIR, 'fields')

LOCALIZED_DIR = os.path.join(BASE_DIR, 'config', 'vocabulary')

# VARIABLES
LOCALIZED = Localized(os.path.join(LOCALIZED_DIR, 'ru.json'))
HELP_MODE = True