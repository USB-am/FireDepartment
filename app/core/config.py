import os


def create_if_not_exists(path: str) -> str:
    if not os.path.exists(path):
        os.mkdir(path)
    return path


DEBUG = True

BASE_DIR = os.getcwd()
ASSETS_DIR = os.path.join(BASE_DIR, 'assets')
IMAGES_DIR = os.path.join(ASSETS_DIR, 'images')
APP_ICON = os.path.join(IMAGES_DIR, 'logo.png')


class KV_PATH:
    BASE_KV_PATH = create_if_not_exists(os.path.join(BASE_DIR, 'kv'))

    KV_SCREEN = create_if_not_exists(os.path.join(BASE_KV_PATH, 'screen'))
    KV_APP = os.path.join(KV_SCREEN, 'app.kv')
    KV_BASE_SCREEN = os.path.join(KV_SCREEN, 'base_screen.kv')


class ApplicationConfig:
    STORAGE_PATH = create_if_not_exists(os.path.join(BASE_DIR, 'storage'))

    USER_PROFILE = os.path.join(STORAGE_PATH, 'user_profile.json')
