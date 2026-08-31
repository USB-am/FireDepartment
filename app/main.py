# -*- coding: utf-8 -*-

from core.config import DEBUG
if DEBUG:
    from kivy.config import Config
    Config.set('graphics', 'width', '360')
    Config.set('graphics', 'height', '650')

from kivy.lang.builder import Builder
from kivy.uix.screenmanager import ScreenManager
from kivymd.app import MDApp
from kivymd.uix.navigationdrawer import MDNavigationLayout

from core.config import KV_PATH, APP_ICON
from service.requests.client import APIClient
from ui import screen as FDScreen
from utils.path_manager import PathManager


Builder.load_file(KV_PATH.KV_APP)


class FDNavigation(MDNavigationLayout):
    ''' Навигация в левом меню '''

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.path_manager = PathManager(self.screen_manager)

        self.ids.main_nav_btn.bind(on_release=lambda *_:
            self.move_screen_and_close_menu('main'))
        self.ids.options_nav_btn.bind(on_release=lambda *_:
            self.move_screen_and_close_menu('options'))
        self.ids.tags_nav_btn.bind(on_release=lambda *_:
            self.move_screen_and_close_menu('tags_list'))
        self.ids.shorts_nav_btn.bind(on_release=lambda *_:
            self.move_screen_and_close_menu('shorts_list'))
        self.ids.ranks_nav_btn.bind(on_release=lambda *_:
            self.move_screen_and_close_menu('ranks_list'))
        self.ids.positions_nav_btn.bind(on_release=lambda *_:
            self.move_screen_and_close_menu('positions_list'))
        self.ids.humans_nav_btn.bind(on_release=lambda *_:
            self.move_screen_and_close_menu('humans_list'))
        self.ids.emergencies_nav_btn.bind(on_release=lambda *_:
            self.move_screen_and_close_menu('emergencies_list'))
        self.ids.worktype_nav_btn.bind(on_release=lambda *_:
            self.move_screen_and_close_menu('worktypes_list'))
        self.ids.history_nav_btn.bind(on_release=lambda *_:
            self.move_screen_and_close_menu('history'))

    def move_screen_and_close_menu(self, screen_name: str) -> None:
        '''
        Перенаправляет на screen_name страницу и закрывает меню.

        :param screen_name: str - имя страницы.
        :returns: None
        '''

        self.path_manager.move_to_screen(screen_name)
        self.ids.menu.set_state('close')

    @property
    def screen_manager(self) -> ScreenManager:
        return self.ids.screen_manager


class MDApplication(MDApp):
    ''' Главный класс приложения '''

    icon = APP_ICON
    title = 'Fire Department'

    def __init__(self):
        super().__init__()

        self.api_client = APIClient(base_url='http://127.0.0.1:8000/api/v1')

        self.ui = FDNavigation()

        # Login screen
        # self.ui.screen_manager.add_widget(FDScreen.FDAuthScreen(self.ui.path_manager))

        # Register screen
        register_screen = FDScreen.FDRegisterScreen(self.ui.path_manager)
        register_screen.set_controller(FDScreen.FDRegisterController(register_screen, self.api_client))
        self.ui.screen_manager.add_widget(register_screen)

        self.ui.path_manager.move_to_screen('register')
    
    def build_config(self, conf):
        conf.setdefaults('options', {
            'primary_palette': self.theme_cls.primary_palette,
            'accent_palette': self.theme_cls.accent_palette,
            'theme_style': self.theme_cls.theme_style,
            'primary_hue': self.theme_cls.primary_hue,
        })

    def build(self):
        conf = self.config
        if conf is not None:
            self.theme_cls.primary_palette = conf.get('options', 'primary_palette')
            self.theme_cls.accent_palette = conf.get('options', 'accent_palette')
            self.theme_cls.theme_style = conf.get('options', 'theme_style')
            self.theme_cls.primary_hue = conf.get('options', 'primary_hue')

        return self.ui


if __name__ == '__main__':
    MDApplication().run()
