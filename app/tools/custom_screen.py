from os import path

from kivy.lang import Builder
from kivy.uix.screenmanager import Screen

from config import TOOLS_DIR, path_manager


path_to_kv_file = path.join(TOOLS_DIR, 'custom_screen.kv')
Builder.load_file(path_to_kv_file)


class CustomScreen(Screen):
	color = (0, 0, 0, 0)
	bg_image = 'C:\\Python\\AndroidApps\\FireDepartment_Finish\\app\\images\\_bg.png'