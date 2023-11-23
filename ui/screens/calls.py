from . import BaseScreen
from app.path_manager import PathManager
from ui.widgets.notebook import FDNotebook


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

		notebook = FDNotebook()
		for i in range(10):
			notebook.add_tab(f'Tab #{i+1}', None)
		self.add_content(notebook)