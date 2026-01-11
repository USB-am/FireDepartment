from typing import List

from requests.exceptions import RequestException

from .base import BaseScrollScreen
from ui.widgets.search import FDSearch
from service.server import send_get
from ui.layout.main_screen import MainScreenListElement, MainScreenInfoElement
from exceptions import NoSecretKeyError


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
        # search.on_press_enter(
        #   callback=lambda text: self.__hide_elements(
        #       filter_list_elements(text)
        #   )
        # )
        self.ids.content_container.add_widget(search)
        self.ids.content_container.children = self.ids.content_container.children[::-1]

        self.elements: List['MainScreenListElement'] = []
        self.fill_elements()
        # self.bind(on_pre_enter=lambda *_: self.__update_elements())
        # self.bind(on_pre_enter=lambda *_: self.__check_new_elements())

    def fill_elements(self) -> None:
        ''' Заполнить контент Вызовами '''
        try:
            emergencies = send_get('model', headers={'model': 'Emergency'}).json()
        except NoSecretKeyError:
            self._path_manager.forward('auth')
            return
        except RequestException as err:
            err_list_element = MainScreenInfoElement(
                title='RequestException',
                description=RequestException.__doc__
            )
            self.add_content(err_list_element)
            return

        for emergency in emergencies:
            list_elem = MainScreenListElement(emergency)
            list_elem.bind_open_button(lambda e=emergency: self.open_call(e))
            self.elements.append(list_elem)
            self.add_content(list_elem)

    def __update_elements(self) -> None:
        ''' Обновить отображенные элементы '''

        for element in self.elements:
            element.update()

    def __hide_elements(self, filtered_elements: List['Emergency']) -> None: # type: ignore
        '''
        Скрыть элементы списка.

        ~params:
        elements: List[Emergency] - записи БД, элементы которых необходимо скрыть.
        '''

        layout: List['MainScreenListElement'] = self.ids.content
        layout.clear_widgets()

        for element in self.elements:
            if element.emergency in filtered_elements:
                self.add_content(element)

    def __check_new_elements(self) -> None:
        ''' Проверка на новые элементы '''

        all_ids = set(entry[0] for entry in \
            Emergency.query.with_entities(Emergency.id).all())
        old_ids = set(e.emergency.id for e in self.elements)

        emergencies_for_insert = all_ids - old_ids
        emergencies_for_delete = old_ids - all_ids
        self.__delete_elements(emergencies_for_delete)
        self.__insert_elements(emergencies_for_insert)

    def __delete_elements(self, emergencies_for_delete: set) -> None:
        '''
        Удалить элементы списка.

        ~params:
        emergencies_for_insert: set - множество элементов для удаления.
        '''

        for element in self.elements:
            if element.emergency.id in emergencies_for_delete:
                self.ids.content.remove_widget(element)
                del element

    def __insert_elements(self, emergencies_for_insert: set) -> None:
        '''
        Вставить элементы списка.

        ~params:
        emergencies_for_insert: set - множество элементов для вставки.
        '''

        for emergency_id in emergencies_for_insert:
            emergency = Emergency.query.get(emergency_id)
            list_elem = MainScreenListElement(emergency)
            list_elem.bind_open_button(lambda e=emergency: self.open_call(e))
            self.elements.append(list_elem)
            self.add_content(list_elem)

        childs = self.ids.content.children
        self.ids.content.children = sorted(
            self.ids.content.children,
            key=lambda child: child.emergency.title,
            reverse=True
        )

    def open_call(self, emergency: 'Emergency') -> None: # type: ignore
        '''
        Переходит на CallsScreen и добавляет вкладку на основании emergency.

        ~params:
        emergency: Emergency - запись из БД о выезде.
        '''

        calls_screen = self._path_manager.forward('calls')
        calls_screen.add_notebook_tab(emergency)
