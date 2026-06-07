from typing import Any

from kivy.properties import ObjectProperty

from . import BaseValidator, ValidatorResult
from ui.widgets.text_input import FDTextInput, FDPasswordInput
from ui.widgets.choice import FDChoice


class TypedObjectProperty(ObjectProperty):
    def __init__(self, property_type: Any, **kwargs):
        super().__init__(**kwargs)
        self.property_type = property_type

    def set(self, obj: Any, value: Any) -> None:
        if value is not None and not isinstance(value, self.property_type):
            raise TypeError(f'{type(obj).__name__} is not {self.property_type.__name__} type!')
        return super().set(obj, value)


class RegisterFormValidator(BaseValidator):
    email_field: FDTextInput
    username_field: FDTextInput
    password_field: FDPasswordInput
    password_again_field: FDPasswordInput
    fire_department_field: FDChoice

    def is_valid(self) -> bool:
        return False
