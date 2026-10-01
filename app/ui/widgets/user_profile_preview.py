from typing import Callable

from kivy.lang.builder import Builder
from kivy.properties import StringProperty
from kivy.uix.widget import Widget
from kivy.uix.behaviors import ButtonBehavior
from kivymd.uix.behaviors import CircularRippleBehavior, HoverBehavior
from kivymd.uix.boxlayout import MDBoxLayout

from core.config import APP_ICON


Builder.load_string('''
<FDUserProfileButton>:
    orientation: 'vertical'
    size_hint: None, None
    size: dp(70), dp(70)
    radius: [dp(12), ]
    padding: [0, dp(8), 0, dp(8)]
    spacing: dp(4)
    md_bg_color: 0, 0, 0, 0
    pos_hint: {'center_y': .5}

    MDIcon:
        icon: root.icon
        halign: 'center'
        size_hint: 1, None
        height: dp(36)
        font_size: dp(36)
        theme_text_color: 'Custom'
        text_color: root.theme_cls.primary_color
        pos_hint: {'center_x': .5}

    MDLabel:
        text: root.text
        size_hint: 1, None
        height: dp(18)
        halign: 'center'
        font_style: 'Caption'
        theme_text_color: 'Secondary'


<FDUserProfilePreview>:
    size_hint: 1, None
    height: dp(265)
    orientation: 'vertical'

    RelativeLayout:
        size_hint: 1, None
        height: dp(185)

        MDLabel:
            id: part_number_lbl
            text: '73'
            halign: 'right'
            size_hint: None, None
            width: self.parent.width - dp(32) if self.parent else root.width - dp(32)
            height: dp(140)
            pos_hint: {'center_y': .5, 'right': 1} 
            font_size: dp(140)         
            bold: True
            theme_text_color: 'Custom'
            text_color: [*root.theme_cls.text_color[:-1], 0.06]

        MDBoxLayout:
            orientation: 'vertical'
            size_hint: 1, 1
            pos_hint: {'x': 0, 'y': 0}
            md_bg_color: 0, 0, 0, 0
            padding: [0, dp(10), 0, 0]
            spacing: dp(6)

            MDAnchorLayout:
                anchor_x: 'center'
                anchor_y: 'center'
                size_hint: None, None
                size: dp(104), dp(104)
                pos_hint: {'center_x': .5}

                canvas.before:
                    Color:
                        rgba: root.theme_cls.primary_color
                    Line:
                        width: dp(2)
                        ellipse: (self.x, self.y, self.width, self.height)

                FitImage:
                    id: avatar
                    source: ''
                    size_hint: None, None
                    size: dp(100), dp(100)
                    radius: [dp(50), ]
                    md_bg_color: .5, .5, .5, .3

            MDLabel:
                id: username_lbl
                size_hint: 1, None
                height: dp(25)
                halign: 'center'
                font_style: 'H6'
                text: ''

            MDLabel:
                id: sign_call_lbl
                size_hint: 1, None
                height: dp(20)
                halign: 'center'
                font_style: 'Body1'
                theme_text_color: 'Secondary'
                text: 'Кама2'

    MDBoxLayout:
        id: button_layout
        orientation: 'horizontal'
        size_hint: 1, None
        height: dp(80)
''')


class FDUserProfileButton(ButtonBehavior, CircularRippleBehavior, HoverBehavior, MDBoxLayout):
    icon = StringProperty('bus')
    text = StringProperty('')

    def __init__(self, **kwargs):
        self.register_event_type('on_release')
        super().__init__(**kwargs)
        self.ripple_color = [1, 1, 1, 0.2]

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            super().on_touch_down(touch)
            self.dispatch('on_release')
            return True
        return super().on_touch_down(touch)

    def on_release(self, *args):
        pass

    def on_enter(self):
        self.md_bg_color = self.theme_cls.divider_color

    def on_leave(self):
        self.md_bg_color = [0, 0, 0, 0]


class FDUserProfilePreview(MDBoxLayout):
    def set_avatar_image(self, path_to_image: str) -> None:
        self.ids.avatar.source = path_to_image

    def set_username(self, username: str) -> None:
        self.ids.username_lbl.text = username

    def set_sign_call(self, sign_call: str) -> None:
        self.ids.sign_call_lbl.text = sign_call

    def add_button(self, icon: str, text: str, callback: Callable) -> None:
        layout = self.ids.button_layout

        if not layout.children:
            layout.add_widget(Widget())

        new_button = FDUserProfileButton(icon=icon, text=text)
        new_button.bind(on_release=callback)

        layout.add_widget(new_button)
        layout.add_widget(Widget())
