import os
import configparser


DEBUG = True

PATH_TO_SERVER = "http://localhost:8000/"

KV_ICONS = {
	"Tag": "pound",
	"Short": "text-short",
	"Rank": "chevron-triple-up",
	"Position": "crosshairs-gps",
	"Human": "account-group",
	"Emergency": "fire-alert",
	"ColorTheme": "palette",
	"Worktype": "timer-sand",
	"UserSettings": "account-wrench",
	"Calls": "firebase",

	"urgent": (
		"fire",
		"fire-alert",
	),
}

BASE_DIR = os.getcwd()

settings = configparser.ConfigParser()
settings.read(os.path.join(BASE_DIR, "app", "application.ini"))

# Assets
ASSETS_DIR = os.path.join(BASE_DIR, "assets")

ICONS_DIR = os.path.join(ASSETS_DIR, "icons")
APP_ICON = os.path.join(ICONS_DIR, "app.png")

IMAGES_DIR = os.path.join(ASSETS_DIR, "images")
LOGO_IMG = os.path.join(IMAGES_DIR, "logo.png")

# Paths to .kv files
KV_DIR = os.path.join(BASE_DIR, "kv")

KV_SCREEN = os.path.join(KV_DIR, 'screen')
KV_APP = os.path.join(KV_SCREEN, "app.kv")
BASE_SCREEN_KV = os.path.join(KV_SCREEN, "based_screen.kv")
