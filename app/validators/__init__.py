from dataclasses import dataclass
from typing import Optional


@dataclass
class BaseValidator:
	error_msg: str = ''


@dataclass
class ValidatorResult:
	status: bool
	message: str


class EmptyValidator(BaseValidator):
	def __call__(self, value: str, message: Optional[str]=None) -> ValidatorResult:
		status = bool(value)

		return ValidatorResult(
			status=status,
			message=message if message is not None else self.error_msg)
