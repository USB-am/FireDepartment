# -*- coding: utf-8 -*-

import os

from kivy.lang import Builder

from config import PATTERNS_DIR
from data_base import Emergency
from app.tools.custom_widgets import CustomScreen


path_to_kv_file = os.path.join(PATTERNS_DIR, 'screens', 'emergency.kv')
Builder.load_file(path_to_kv_file)


class EmergencyPage(CustomScreen):
	name = 'emergency_page'
	table = Emergency

	def __init__(self):
		super().__init__()