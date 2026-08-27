from dataclasses import dataclass
from abc import ABC, abstractmethod


@dataclass
class ValidatorResult:
    status: bool
    message: str


@dataclass
class BaseValidator(ABC):
    error_msg: str = ''

    @abstractmethod
    def __call__(self, value: str, message: str | None=None) -> ValidatorResult:
        pass
