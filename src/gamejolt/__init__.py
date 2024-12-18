"""
A python wrapper for the gamejolt API.

This library provides a simple to use interface for interacting with the gamejolt
API. It includes a requester class that can be used to make requests to the
API, and a formatter class that can be used to format URL's for the API.

The library is designed to be easy to use and will automatically generate
the signature for the request and append it to the URL.
"""

from .endpoints import Formatter, Endpoints
from .requester import RequesterAbstract

__all__ = ["GameJolt", "Formatter", "Endpoints", "RequesterAbstract"]


from .subcomponents import UsersComponent


# pylint: disable=W0223
class GameJolt(RequesterAbstract):
    """A class for interacting with the Game Jolt API.
    a single namespace for all the subcomponents.
    """

    def __init__(self, key: str, *args, **kw) -> None:
        super().__init__(key, *args, **kw)
        self.users = UsersComponent(self)
