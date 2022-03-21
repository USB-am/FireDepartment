# -*- coding: utf-8 -*-

import os

from kivy.uix.screenmanager import Screen
from kivy.lang import Builder

import config as Config


Builder.load_file(os.path.join(Config.PATTERNS_DIR, 'settings.kv'))


class Settings(Screen):
	name = 'settings'