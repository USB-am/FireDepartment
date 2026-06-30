from ui.screen.based_screen import BaseScrollScreen


class FDMainScreen(BaseScrollScreen):
    name = 'main'
    title = 'Fire Department'

    controller = None

    def __init__(self, path_manager: 'PathManager'):
        super().__init__(path_manager)

        self.add_left_toolbar_items('menu', self.open_menu)
        self.add_right_toolbar_items('fire-truck', lambda *_: print('open journal screen'))
