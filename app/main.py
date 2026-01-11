# -*- coding: utf-8 -*-

from kivy.config import Config
Config.set('graphics', 'width', '360')
Config.set('graphics', 'height', '650')

from kivymd.app import MDApp
from kivy.lang.builder import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.uix.navigationdrawer import MDNavigationLayout

import config
from ui import screens as FDScreen
from service.singleton import _Singleton


Builder.load_file(config.APP_SCREEN)


class PathManager(metaclass=_Singleton):
    ''' Менеджер путей '''

    def __init__(self, screen_manager: ScreenManager):
        self.__screen_manager = screen_manager
        self._path = ['main',]

    def forward(self, screen_name: str) -> Screen:
        self.__screen_manager.current = screen_name
        self._path.append(screen_name)
        print(self._path)

        return self.__screen_manager.current_screen

    def back(self) -> Screen:
        if len(self._path) > 1:
            self._path.pop(-1)

        self.__screen_manager.current = self._path[-1]
        print(self._path)

        return self.__screen_manager.current_screen

    def move_to_screen(self, screen_name: str) -> Screen:
        self._path = []
        return self.forward(screen_name)


class FDNavigation(MDNavigationLayout):
    ''' Навигация в левом меню '''

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.path_manager = PathManager(self.screen_manager)

        self.ids.main_nav_btn.bind(on_release=lambda *_:
            self.move_screen_and_close_menu('main'))
        # self.ids.options_nav_btn.bind(on_release=lambda *_:
        #     self.move_screen_and_close_menu('options'))
        # self.ids.tags_nav_btn.bind(on_release=lambda *_:
        #     self.move_screen_and_close_menu('tags_list'))
        # self.ids.shorts_nav_btn.bind(on_release=lambda *_:
        #     self.move_screen_and_close_menu('shorts_list'))
        # self.ids.ranks_nav_btn.bind(on_release=lambda *_:
        #     self.move_screen_and_close_menu('ranks_list'))
        # self.ids.positions_nav_btn.bind(on_release=lambda *_:
        #     self.move_screen_and_close_menu('positions_list'))
        # self.ids.humans_nav_btn.bind(on_release=lambda *_:
        #     self.move_screen_and_close_menu('humans_list'))
        # self.ids.emergencies_nav_btn.bind(on_release=lambda *_:
        #     self.move_screen_and_close_menu('emergencies_list'))
        # self.ids.worktype_nav_btn.bind(on_release=lambda *_:
        #     self.move_screen_and_close_menu('worktypes_list'))
        # self.ids.history_nav_btn.bind(on_release=lambda *_:
        #     self.move_screen_and_close_menu('history'))

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


class Application(MDApp):
    icon = config.APP_ICON
    title = 'Fire Department'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.ui = FDNavigation()

        self.ui.screen_manager.add_widget(FDScreen.MainScreen(self.ui.path_manager))
        self.ui.screen_manager.add_widget(FDScreen.AuthScreen(self.ui.path_manager))
        self.ui.screen_manager.add_widget(FDScreen.RegisterScreen(self.ui.path_manager))

        self.ui.path_manager.move_to_screen('main')

    def build_config(self, conf):
        conf.setdefaults('options', {
            'primary_palette': self.theme_cls.primary_palette,
            'accent_palette': self.theme_cls.accent_palette,
            'theme_style': self.theme_cls.theme_style,
            'primary_hue': self.theme_cls.primary_hue,
        })
        conf.setdefaults('call', {
            'work_day_ignore': '1',
            'start_text': '[HH:MM dd.mm.yyyy] Начало выезда.',
            'finish_text': '[HH:MM dd.mm.yyyy] Конец выезда.',
            'human_success': '[HH:MM dd.mm.yyyy] Вызов {human_name}.',
            'human_unsuccess': '[HH:MM dd.mm.yyyy] Вызов {human_name} не прошел.',
        })

    def build(self):
        conf = self.config
        self.theme_cls.primary_palette = conf.get('options', 'primary_palette')
        self.theme_cls.accent_palette = conf.get('options', 'accent_palette')
        self.theme_cls.theme_style = conf.get('options', 'theme_style')
        self.theme_cls.primary_hue = conf.get('options', 'primary_hue')

        return self.ui


if __name__ == '__main__':
    Application().run()
