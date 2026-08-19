from enum import Enum


class Role(Enum):
    admin = 'admin'
    manager = 'manager'
    dispatch = 'dispatch'
    reader = 'reader'
