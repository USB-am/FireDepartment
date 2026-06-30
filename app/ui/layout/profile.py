from typing import Callable

from kivy.lang.builder import Builder
from kivymd.uix.boxlayout import MDBoxLayout

from config import KV_PROFILE


Builder.load_file(KV_PROFILE)


class FDProfileLayout(MDBoxLayout):
    ''' Поле с информацией о профиле пользователя '''

    def __init__(self, title: str, **options):
        self.title = title

        super().__init__(**options)

        self._button_callback = None

    def update(self, user: 'UserProfileData') -> None:
        self.ids.username_field.text = user.username
        self.ids.email_field.text = user.email
        self.ids.firedepartment_field.text = user.firedepartment

        # self.ids.bg_label.text = user.fd_number

        if user.avatar:
            self.ids.avatar_image.source = user.avatar
            self.ids.avatar_image.opacity = 1
            # self.ids.avatar_icon.opacity = 0
        else:
            self.ids.avatar_image.source = ''
            self.ids.avatar_image.opacity = 0
            # self.ids.avatar_icon.opacity = 1

    def bind_button(self, callback: Callable) -> None:
        self._button_callback = callback

    def _on_change_button(self) -> None:
        if self._button_callback:
            self._button_callback()
