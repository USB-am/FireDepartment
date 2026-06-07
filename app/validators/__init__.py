from dataclasses import dataclass


@dataclass
class BaseValidator:
	error_msg: str = ''


@dataclass
class ValidatorResult:
	status: bool
	message: str
