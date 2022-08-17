import os

from kivy.lang import Builder
from kivymd.uix.boxlayout import MDBoxLayout

from config import UIX_KV_DIR, LOCALIZED


path_to_kv_file = os.path.join(UIX_KV_DIR, 'search_block.kv')
Builder.load_file(path_to_kv_file)


class FDSearchBlock(MDBoxLayout):
	''' Блок поиска '''

	def __init__(self):
		self.placeholder = LOCALIZED.translate('Search')

		super().__init__()