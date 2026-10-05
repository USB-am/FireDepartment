from kivy.lang.builder import Builder
from kivy.properties import StringProperty, ListProperty
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.menu import MDDropdownMenu


Builder.load_string('''
<FDDropDownMenu>:
    orientation: 'horizontal'
    size_hint: 1, None
    height: dp(50)

    MDLabel:
        size_hint: 1, None
        height: root.height
        text: root.title
        valign: 'middle'

    MDRectangleFlatButton:
        id: menu_btn
        text: root.default
        on_release: root.menu.open()
''')


class FDDropDownMenu(MDBoxLayout):
    title: str = StringProperty()
    default: str = StringProperty('<Empty>')
    items: list[dict] = ListProperty()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.menu = MDDropdownMenu(
            caller=self.ids.menu_btn,
            items=self.items,
            width_mult=4
        )
