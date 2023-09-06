from dataclasses import dataclass

from everyday_joke.business.base import Interactor

from .base import AppException


@dataclass
class UserNotFound(AppException):
    user_id: int
    on_process: None | Interactor = None
