from dataclasses import dataclass
from typing import Optional

from . import BaseValidator, ValidatorResult
from email_validator import validate_email, EmailNotValidError


class EmptyValidator(BaseValidator):
	def __call__(self, value: str, message: Optional[str]=None) -> ValidatorResult:
		status = bool(value)

		return ValidatorResult(
			status=status,
			message=message if message is not None else self.error_msg)


class EmailValidator(BaseValidator):
	def __call__(self, value: str, message: Optional[str]=None) -> ValidatorResult:
		try:
			validate_email(value, check_deliverability=False)
			status = True
		except EmailNotValidError:
			status = False

		return ValidatorResult(
			status=status,
			message=message if message is not None else self.error_msg)


class IdenticalPasswords(BaseValidator):
	def __call__(self, value_1: str, value_2: str, message: Optional[str]=None) -> ValidatorResult:
		status = value_1 == value_2

		return ValidatorResult(
			status=status,
			message=message if message is not None else self.error_msg)
