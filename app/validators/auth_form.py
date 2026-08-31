from typing import Any

from . import BaseValidator
from ui.widgets.text_field import FDTextInput, FDPasswordInput


class FDTypedFieldDescriptor:
    def __init__(self, expected_type: Any):
        self.expected_type = expected_type

    def __set_name__(self, owner: Any, name: str) -> None:
        self.name = name

    def __get__(self,
                instance: 'FDTypedFieldDescriptor',
                owner: Any
) -> 'FDTypedFieldDescriptor | str | None':

        if instance is None:
            return self
        return instance.__dict__.get(self.name)
    
    def __set__(self, instance, value):
        if not isinstance(value, self.expected_type):
            raise TypeError

        instance.__dict__[self.name] = value


class AuthFormValidator(BaseValidator):
    email_field = FDTypedFieldDescriptor(FDTextInput)
    password_field = FDTypedFieldDescriptor(FDPasswordInput)

    def __init__(self,
                 email_field,
                 password_field,
                 **kwargs):

        super().__init__(**kwargs)

        self.email_field = email_field
        self.password_field = password_field

        self._all_fields = [
            email_field,
            password_field,
        ]

    def __call__(self, *_) -> None:
        pass

    def is_valid(self) -> bool:
        return all(map(lambda field: not field.error, self._all_fields))
