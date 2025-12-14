from typing import Type, Callable, List, Dict

from kivy.lang.builder import Builder
from kivy.properties import BooleanProperty, StringProperty
from kivy.uix.recycleview import RecycleView
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivymd.uix.boxlayout import MDBoxLayout

from config import SELECT_FIELD


Builder.load_file(SELECT_FIELD)


class TempModel:
	icon = 'bus'
	query = ['Hello', 'World!']


class _BaseSelect(MDBoxLayout):
	'''
	Поле выбора нескольких элементов из модели БД.

	~params:
	title: str - текст над списком;
	dialog_content: MDBoxLayout - содержимое окна с информацией;
	model: db.Model - модель БД, элементы которой будут отображены;
	group: str=None - группа объектов. Если None, доступен выбор множества элементов.
	'''

	def __init__(self, title: str, dialog_content: MDBoxLayout, model, group: str):
		self.title = title
		self.dialog_content = dialog_content
		self.model = model
		self.group = group

		super().__init__()

		self.elements: List[FDSelectListElement] = []
		self.callbacks: List[Callable] = []
		self.fill_elements()

	def fill_elements(self) -> None:
		''' Заполняет список недостающими элементами из модели '''

		all_entries = self.model.query.order_by(self.model.title)
		entries = filter_created_widgets(self.elements, set(all_entries))
		sorted_entries = sorted(entries, key=lambda e: e.title)

		for entry in sorted_entries:
			list_elem = FDSelectListElement(
				entry=entry,
				info_content=self.dialog_content,
				group=self.group)

			for callback in self.callbacks:
				list_elem.ids.checkbox.bind(on_release=lambda *_: callback())

			self.elements.append(list_elem)
			self.ids.content.add_widget(list_elem)

	def bind_btn(self, callback: Callable) -> None:
		''' Привязать событие нажатия кнопки на верхней панели '''

		self.ids.add_btn.bind(on_release=lambda *_: callback())

	def bind_checkbox(self, callback: Callable) -> None:
		''' Привязать событие нажатия чекбокса '''

		self.callbacks.append(callback)

		for element in self.elements:
			element.ids.checkbox.bind(on_release=lambda *_: callback())


class FDSelectElement(RecycleDataViewBehavior, MDBoxLayout):
	''' Элемент списка FDSelect '''

	index = None
	text = StringProperty()
	group = StringProperty(None)
	active = BooleanProperty()

	def refresh_view_attrs(self, rv, index, data):
		self.index = index
		return super().refresh_view_attrs(rv, index, data)

	def store_checkbox_state(self):
		rv = self.parent.parent
		rv.update_checkbox_state(index=self.index,
		                         state=self.active,
		                         group=self.group)


class SelectableRecycleBoxLayout(FocusBehavior, LayoutSelectionBehavior, RecycleBoxLayout):
	''' Предстваление области отображения элементов списка '''


class _FDSelectRecycleView(RecycleView):
	''' Вьюха списка элементов '''

	def update_checkbox_state(self, index: int, state: bool, group: str) -> None:
		''' Обновить состояния чекбоксов '''

		if group:
			for elem in self.data:
				if elem['active']:
					elem['active'] = False
		self.data[index]['active'] = state


class _BaseRecycleSelect(_BaseSelect):
	''' Оптимизированный FDSelect '''

	def __init__(self, data: List[Dict], **options):
		super().__init__(**options)
		self.ids.recycle_view.data = data

		self.bind_btn(lambda *_: print(self.get_value()))

	@property
	def data(self) -> List[Dict]:
		return self.ids.recycle_view.data

	def fill_elements(self) -> None:
		''' Заполняет список недостающими элементами из модели '''

		# TODO


class FDRecycleSelect(_BaseRecycleSelect):
	''' Поле выбора одного элемента.

	~params:
	title: str - текст над списком;
	dialog_content: MDBoxLayout - содержимое окна с информацией;
	model: db.Model - модель БД, элементы которой будут отображены;
	group: str - группа объектов. Если None, доступен выбор множества элементов.
	'''

	def get_value(self) -> int:
		''' Получить id выбранного элемента '''

		try:
			return next(filter(lambda elem: elem['active'], self.data))
		except StopIteration:
			return None


class FDRecycleMultiSelect(_BaseRecycleSelect):
	''' Поле выбора множества элементов '''

	def __init__(self, **kwargs):
		kwargs.update({'group': None})
		super().__init__(**kwargs)

	def get_value(self) -> List:
		''' Получить записи о выбранных элементах '''

		filtered_elems = filter(lambda elem: elem['active'], self.data)
		return list(map(lambda elem: elem['text'], filtered_elems))
