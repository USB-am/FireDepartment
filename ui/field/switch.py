from kivy.lang.builder import Builder
from kivy.properties import StringProperty
from kivymd.uix.boxlayout import MDBoxLayout

from config import SWITCH_FIELD


Builder.load_file(SWITCH_FIELD)


class FDDoubleSwitch(MDBoxLayout):
	'''
	Переключатель с переключаемыми иконками.

	~params:
	icon_active: str - активная иконка;
	icon_deactive: str - деактивированная иконка;
	title_active: str - активный заголовок;
	title_deactive: str - деактивированный заголовок.
	'''

	icon_active = StringProperty()
	icon_deactive = StringProperty()
	title_active = StringProperty()
	title_deactive = StringProperty()

	def _pressed_to_switch(self) -> None:
		icon = self.ids.icon
		title = self.ids.title

		if self.ids.switch.active:
			icon.icon = self.icon_active
			title.text = self.title_active
		else:
			icon.icon = self.icon_deactive
			title.text = self.title_deactive
