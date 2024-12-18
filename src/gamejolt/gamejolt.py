"""This module provides the GameJolt class for interacting with the Game Jolt API."""

from .requester import RequesterAbstract
from .subcomponents import UsersComponent


# pylint: disable=W0223
class GameJolt(RequesterAbstract):
    def __init__(self, key: str, *args, **kw) -> None:
        super().__init__(key, *args, **kw)
        self.users = UsersComponent(self)
