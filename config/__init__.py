import os

from .localized import Localized


BASE_DIR = os.getcwd()

# KV DIRS
KV_DIR = os.path.join(BASE_DIR, 'kv')
UIX_KV_DIR = os.path.join(KV_DIR, 'uix')

# LOCALIZED DIRS
LOCALIZED_DIR = os.path.join(BASE_DIR, 'config', 'vocabulary')

LOCALIZED = Localized(os.path.join(LOCALIZED_DIR, 'ru.json'))