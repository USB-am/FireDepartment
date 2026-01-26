from typing import List
from dataclasses import dataclass, field

from requests.exceptions import RequestException

from .base import BaseScrollScreen
from ui.widgets.search import FDSearch
from service.server import send_get
from ui.layout.main_screen import MainScreenListElement, MainScreenInfoElement
from exceptions import NoSecretKeyError


@dataclass
class Emergency:
    id: int
    title: str
    description: str
    urgent: bool
    tags: list = field(default_factory=list)
    humans: list = field(default_factory=list)
    calls: list = field(default_factory=list)
    shorts: list = field(default_factory=list)


class MainScreen(BaseScrollScreen):
    ''' Стартовая страница '''

    name = 'main'
    toolbar_title = 'Главная'

    def __init__(self, path_manager: 'PathManager', **options):
        super().__init__(path_manager)

        self.ids.toolbar.add_left_button(
            icon='menu',
            callback=self.open_menu
        )
        self.ids.toolbar.add_right_button(
            icon='fire-truck',
            callback=lambda *_: self._path_manager.forward('calls')
        )

        search = FDSearch(hint_text='Поиск...')
        search.on_press_enter(callback=lambda text: self.fill_elements(search_text=text))
        self.ids.content_container.add_widget(search)
        self.ids.content_container.children = self.ids.content_container.children[::-1]

        self.elements: List['MainScreenListElement'] = []
        self.fill_elements()

    def fill_elements(self, search_text: str='') -> None:
        ''' Заполнить контент Вызовами '''
        self.clear_content()

        try:
            emergencies = send_get('model', params={'model': 'Emergency', 'q': search_text}).json()
        except NoSecretKeyError:
            self._path_manager.forward('auth')
            return
        except RequestException as err:
            err_list_element = MainScreenInfoElement(
                title='RequestException',
                description=RequestException.__doc__
            )
            self.add_content(err_list_element)
            self._path_manager.forward('auth')
            return

        for emergency_dict in emergencies:
            emergency = Emergency(**emergency_dict)
            list_elem = MainScreenListElement(emergency)
            list_elem.bind_open_button(lambda e=emergency: self.open_call(e))
            self.elements.append(list_elem)
            self.add_content(list_elem)

    def __update_elements(self) -> None:
        ''' Обновить отображенные элементы '''
        map(lambda e: e.update(), self.elements)

    def open_call(self, emergency: 'Emergency') -> None: # type: ignore
        '''
        Переходит на CallsScreen и добавляет вкладку на основании emergency.

        ~params:
        emergency: Emergency - запись из БД о выезде.
        '''

        calls_screen = self._path_manager.forward('calls')
        calls_screen.add_notebook_tab(emergency)
