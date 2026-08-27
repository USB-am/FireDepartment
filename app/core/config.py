import os
from dataclasses import dataclass


DEBUG = True

BASE_DIR = os.getcwd()
ASSETS_DIR = os.path.join(BASE_DIR, 'assets')
IMAGES_DIR = os.path.join(ASSETS_DIR, 'images')
APP_ICON = os.path.join(IMAGES_DIR, 'logo.png')


class KV_PATH:
    BASE_KV_PATH = os.path.join(BASE_DIR, 'kv')

    KV_SCREEN = os.path.join(BASE_KV_PATH, 'screen')
    KV_APP = os.path.join(KV_SCREEN, 'app.kv')
    KV_BASE_SCREEN = os.path.join(KV_SCREEN, 'base_screen.kv')
