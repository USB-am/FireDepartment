from . import BaseScreen
from app.path_manager import PathManager
from ui.widgets.notebook import FDNotebook

from data_base import Emergency


class CallsScreen(BaseScreen):
	'''
	Страница текущих вызовов
	'''

	name = 'calls'
	toolbar_title = 'Вызовы'

	def __init__(self, path_manager: PathManager, **options):
		super().__init__(path_manager)

		self.ids.toolbar.add_left_button(
			icon='arrow-left',
			callback=lambda *_: self._path_manager.back()
		)

		self.notebook = FDNotebook()
		self.add_content(self.notebook)
