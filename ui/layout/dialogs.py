from datetime import date, datetime
from calendar import Calendar

from kivy.lang.builder import Builder
from kivy.properties import ObjectProperty
from kivy.uix.widget import Widget
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.dialog import MDDialog

from app.path_manager import PathManager
from config import DIALOG_LAYOUTS
from data_base import db, Tag, Rank, Position, Human, Emergency, Worktype, \
	Short, Calls
from ui.field.label import FDTitle, FDVerticalLabel, FDDoubleVerticalLabel
from ui.field.button import FDIconButton
from ui.field.calendar import is_work_day, add_months


Builder.load_file(DIALOG_LAYOUTS)


class _BaseDialogContent(MDBoxLayout):
	'''
	Базовый класс содержимого всплывающего окна.

	~params:
	entry: db.Model - запись из модели.
	'''

	entry = ObjectProperty(defaultvalue=db.Model)

	def add_content(self, widget: Widget) -> None:
		'''
		Добавляет виджет на фрейм контента.

		~params:
		widget: Widget - виджет, который будет отображен.
		'''

		self.ids.content.add_widget(widget)

	def _move_to_screen(self, page_ref: str, entry: db.Model) -> None:
		'''
		Переход на экран.

		~params:
		page_ref: str - name экрана перехода;
		entry: db.Model - запись из БД.
		'''

		screen = PathManager().forward(page_ref)
		screen.fill_fields(entry)
		parent_dialog: MDDialog = self.parent.parent.parent
		parent_dialog.dismiss()


class ConfirmDialogContent(_BaseDialogContent):
	'''
	Представление содержимого диалогового окна с подтверждением.
	'''

	def __init__(self, entry: db.Model, text: str, **options):
		self.text = text
		super().__init__(entry=entry, **options)

		self.ids.content.add_widget(FDVerticalLabel(
			title='Предупреждение!',
			value=text))


class TagDialogContent(_BaseDialogContent):
	'''
	Содержимое всплывающего окна с информацией о записи из модели Tag.

	~params:
	entry: Tag - запись из модели Tag.
	'''

	def __init__(self, entry: Tag, **options):
		super().__init__(entry=entry, **options)

		self.ids.content.add_widget(FDVerticalLabel(
			title='Название',
			value=entry.title))

		if entry.emergencys:
			self.ids.content.add_widget(FDTitle(
				title='Связан с Вызовами:'))

			sorted_emergencies = sorted(entry.emergencys, key=lambda e: e.title)
			for emergency in sorted_emergencies:
				btn = FDIconButton(
					icon=emergency.icon,
					icon_btn='eye',
					title=emergency.title
				)
				btn.bind_btn(lambda e=emergency: self._move_to_screen('edit_emergency', e))

				self.ids.content.add_widget(btn)


class ShortDialogContent(_BaseDialogContent):
	'''
	Содержимое всплывающего окна с информацией о записи из модели Short.

	~params:
	entry: Short - запись из модели Short.
	'''

	def __init__(self, entry: Short, **options):
		super().__init__(entry=entry, **options)

		self.ids.content.add_widget(FDVerticalLabel(
			title='Название',
			value=entry.title))
		self.ids.content.add_widget(FDVerticalLabel(
			title='Полный текст',
			value=entry.explanation))
		if entry.emergencys:
			self.ids.content.add_widget(FDTitle(
				title='Связан с Вызовами:'))

			sorted_emergencies = sorted(entry.emergencys, key=lambda e: e.title)
			for emergency in sorted_emergencies:
				btn = FDIconButton(
					icon=emergency.icon,
					icon_btn='eye',
					title=emergency.title
				)
				btn.bind_btn(lambda e=emergency: self._move_to_screen('edit_emergency', e))

				self.ids.content.add_widget(btn)


class RankDialogContent(_BaseDialogContent):
	'''
	Содержимое всплывающего окна с информацией о записи из модели Rank.

	~params:
	entry: Rank - запись из модели Rank.
	'''

	def __init__(self, entry: Rank, **options):
		super().__init__(entry=entry, **options)

		self.ids.content.add_widget(FDVerticalLabel(
			title='Название',
			value=entry.title))
		self.ids.content.add_widget(FDVerticalLabel(
			title='Приоритет',
			value=str(entry.priority)))


class PositionDialogContent(_BaseDialogContent):
	'''
	Содержимое всплывающего окна с информацией о записи из модели Position.

	~params:
	entry: Position - запись из модели Position.
	'''

	def __init__(self, entry: Position, **options):
		super().__init__(entry=entry, **options)

		self.ids.content.add_widget(FDVerticalLabel(
			title='Название',
			value=entry.title))

		if entry.humans:
			self.ids.content.add_widget(FDTitle(
				title='Связан с Людьми:'))

			sorted_humans = sorted(entry.humans, key=lambda h: h.title)
			for human in sorted_humans:
				btn = FDIconButton(
					icon=human.icon,
					icon_btn='eye',
					title=human.title
				)
				btn.bind_btn(lambda h=human: self._move_to_screen('edit_human', h))
				self.ids.content.add_widget(btn)


class HumanDialogContent(_BaseDialogContent):
	'''
	Содержимое всплывающего окна с информацией о записи из модели Human.

	~params:
	entry: Human - запись из модели Human.
	'''

	def __init__(self, entry: Human, **options):
		super().__init__(entry=entry, **options)

		self.ids.content.add_widget(FDVerticalLabel(
			title='ФИО',
			value=entry.title))

		if entry.phone_1 is not None:
			self.ids.content.add_widget(FDVerticalLabel(
				title='Телефон',
				value=entry.phone_1))

		if entry.phone_2 is not None:
			self.ids.content.add_widget(FDVerticalLabel(
				title='Телефон (доп.)',
				value=entry.phone_2))

		position_id = entry.position
		if position_id is not None:
			position = Position.query.get(position_id)
			self.ids.content.add_widget(FDVerticalLabel(
				title='Должность',
				value=position.title))

		rank_id = entry.rank
		if rank_id is not None:
			rank = Rank.query.get(rank_id)
			self.ids.content.add_widget(FDVerticalLabel(
				title='Звание',
				value=rank.title))

		self.ids.content.add_widget(FDVerticalLabel(
			title='Пожарный',
			value='Да' if entry.is_firefigher else 'Нет'))

		self.ids.content.add_widget(FDVerticalLabel(
			title='Следующий рабочий день',
			value=self.next_work_day))

		if entry.worktype is None:
			worktype_title = 'Неизвестно'
		else:
			worktype_title = Worktype.query.get(entry.worktype).title
		self.ids.content.add_widget(FDVerticalLabel(
			title='График работы',
			value=worktype_title))

	@property
	def next_work_day(self) -> str:
		''' Возвращает следующий рабочий день '''

		if self.entry.worktype is None:
			return 'Неизвестно'

		current_date = datetime.now().date()
		next_month_date = add_months(current_date=current_date, months_to_add=1)
		now_month_days = Calendar().itermonthdates(current_date.year,
		                                           current_date.month)
		next_month_days = Calendar().itermonthdates(next_month_date.year,
		                                            next_month_date.month)
		month_days = sorted(set(list(now_month_days) + list(next_month_days)))

		for day in month_days:
			if day <= current_date:
				continue

			if is_work_day(day, self.entry.work_day, Worktype.query.get(self.entry.worktype)):
				return day.strftime('%d.%m.%Y')


class EmergencyDialogContent(_BaseDialogContent):
	'''
	Содержимое всплывающего окна с информацией о записи из модели Emergency.

	~params:
	entry: Emergency - запись из модели Emergency.
	'''

	def __init__(self, entry: Emergency, **options):
		super().__init__(entry=entry, **options)

		self.ids.content.add_widget(FDVerticalLabel(
			title='Название',
			value=entry.title))

		if entry.urgent:
			self.ids.content.add_widget(FDVerticalLabel(
				title='',
				value='Срочный!'))

		if entry.humans:
			self.ids.content.add_widget(FDTitle(
				title=f'Задействовано людей: {len(entry.humans)}'))

			sorted_humans = sorted(entry.humans, key=lambda h: h.title)
			for human in sorted_humans:
				btn = FDIconButton(
					icon=human.icon,
					icon_btn='eye',
					title=human.title
				)
				btn.bind_btn(lambda h=human: self._move_to_screen('edit_human', h))

				self.ids.content.add_widget(btn)


class WorktypeDialogContent(_BaseDialogContent):
	'''
	Содержимое всплывающего окна с информацией о записи из модели Worktype.

	~params:
	entry: Worktype - запись из модели Worktype.
	'''

	def __init__(self, entry: Worktype, **options):
		super().__init__(entry=entry, **options)

		self.ids.content.add_widget(FDVerticalLabel(
			title='Название',
			value=entry.title))
		self.ids.content.add_widget(FDVerticalLabel(
			title='Начало рабочего дня',
			value=entry.start_work_day.time().strftime('%H:%M:%S')))
		self.ids.content.add_widget(FDVerticalLabel(
			title='Конец рабочего дня',
			value=entry.finish_work_day.time().strftime('%H:%M:%S')))
		self.ids.content.add_widget(FDVerticalLabel(
			title='Рабочих дней подряд',
			value=str(entry.work_day_range)))
		self.ids.content.add_widget(FDVerticalLabel(
			title='Выходных подряд',
			value=str(entry.week_day_range)))

		if entry.humans:
			self.ids.content.add_widget(FDTitle(
				title=f'Задействовано людей: {len(entry.humans)}'))

			sorted_humans = sorted(entry.humans, key=lambda h: h.title)
			for human in sorted_humans:
				btn = FDIconButton(
					icon=human.icon,
					icon_btn='eye',
					title=human.title
				)
				btn.bind_btn(lambda h=human: self._move_to_screen('edit_human', h))

				self.ids.content.add_widget(btn)


class CallsDialogContent(_BaseDialogContent):
	'''
	Содержимое всплывающего окна с информацией о записи из модели Calls.

	~params:
	entry: Calls - запись из модели Calls.
	'''

	def __init__(self, entry: Calls, **options):
		super().__init__(entry=entry, **options)

		self.add_content(FDVerticalLabel(
			title='Название Выезда',
			value=Emergency.query.get(entry.emergency).title
		))
		self.add_content(FDDoubleVerticalLabel(
			title_1='Начало',
			value_1=entry.start.strftime('%H:%M %d.%m.%Y'),
			title_2='Конец',
			value_2=entry.finish.strftime('%H:%M %d.%m.%Y')
		))
		self.add_content(FDTitle(
			title='Информация:'
		))
		self.add_content(MDLabel(
			text=entry.info + ' ',
			adaptive_height=True
		))
