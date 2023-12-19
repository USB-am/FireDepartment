from kivy.lang.builder import Builder
from kivy.properties import ObjectProperty
from kivy.uix.widget import Widget
from kivymd.uix.boxlayout import MDBoxLayout

from config import DIALOG_LAYOUTS
from data_base import db, Tag, Rank, Position, Human, Emergency, Worktype
from ui.field.label import FDTitle, FDVerticalLabel
from ui.field.button import FDIconButton


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
				btn.bind_btn(lambda e=emergency: print(f'View {e.title} emergency'))

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
				btn.bind_btn(lambda h=human: print(f'View {h.title} human'))
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

		# TODO: set value
		self.ids.content.add_widget(FDVerticalLabel(
			title='Следующий рабочий день',
			value=''))

		if entry.worktype is None:
			worktype_title = 'Неизвестно'
		else:
			worktype_title = Worktype.query.get(entry.worktype).title
		self.ids.content.add_widget(FDVerticalLabel(
			title='График работы',
			value=worktype_title))


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
				btn.bind_btn(lambda h=human: print(f'View {h.title} human'))

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
				btn.bind_btn(lambda h=human: print(f'View {h.title} human'))

				self.ids.content.add_widget(btn)
