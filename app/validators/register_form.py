from typing import Any, Optional, Union
from dataclasses import dataclass

from kivy.properties import ObjectProperty

from . import BaseValidator, ValidatorResult
from ui.widgets.text_input import FDTextInput, FDPasswordInput
from ui.widgets.choice import FDChoice


class FDTypedFieldDescriptor:
    def __init__(self, expected_type: Optional[Any]):
        self.expected_type = expected_type
        self.name = None

    def __set_name__(self, owner, name: str) -> None:
        print(f'{owner=}')
        self.name = name

    def __get__(self, instance: 'FDFieldDescriptor', owner) -> Optional[Union['FDFieldDescriptor', str]]:
        if instance is None:
            return self
        return instance.__dict__.get(self.name)
    
    def __set__(self, instance, value):
        if not isinstance(value, self.expected_type):
            raise TypeError

        instance.__dict__[self.name] = value


class TypedObjectProperty(ObjectProperty):
    def __init__(self, property_type: Any, **kwargs):
        super().__init__(**kwargs)
        self.property_type = property_type

    def set(self, obj: Any, value: Any) -> None:
        if value is not None and not isinstance(value, self.property_type):
            raise TypeError(f'{type(obj).__name__} is not {self.property_type.__name__} type!')
        return super().set(obj, value)


class RegisterFormValidator(BaseValidator):
    email_field = FDTypedFieldDescriptor(FDTextInput)
    username_field = FDTypedFieldDescriptor(FDTextInput)
    password_field = FDTypedFieldDescriptor(FDPasswordInput)
    password_again_field = FDTypedFieldDescriptor(FDPasswordInput)
    fire_department_field = FDTypedFieldDescriptor(FDChoice)

    def __init__(self,
                 email_field,
                 username_field,
                 password_field,
                 password_again_field,
                 fire_department_field,
                 **kwargs):
        super().__init__(**kwargs)
        self.email_field = email_field
        self.username_field = username_field
        self.password_field = password_field
        self.password_again_field = password_again_field
        self.fire_department_field = fire_department_field

        print(self.email_field.get_value())

    def is_valid(self) -> bool:
        return False
