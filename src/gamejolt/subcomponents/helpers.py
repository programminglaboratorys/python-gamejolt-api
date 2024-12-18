"""This module provides a helper functions"""

from typing import Iterable
from functools import wraps
from ..constants import VERSIONS
from ..models import User


def instance_checker(type: type, iterable: Iterable):
    """
    Checks if any element in the iterable is an instance of a given type.

    This function takes a type and an iterable, and checks if any element
    in the iterable is an instance of the specified type. It returns True
    if at least one element matches the type, otherwise False.

    :param type: The type to check against.
    :type type: type
    :param iterable: An iterable containing elements to check.
    :type iterable: Iterable
    :return: True if any element is an instance of the specified type, otherwise False.
    :rtype: bool
    """

    return any(map(lambda obj: isinstance(obj, type), iterable))


def api_version_guard(api_version: str):
    """
    Decorator for checking API version.

    This decorator takes a method and the API version the method is
    supported on.

    :param api_version: The API version the method is supported on.
    :type api_version: str

    :raise ValueError: If the API version does not match the one the method is supported on.
    """

    def wrapper(func):
        @wraps(func)
        def inner(self, *args, **kwargs):
            if VERSIONS[self.requester.api_version] < VERSIONS[api_version]:
                raise ValueError(
                    f"API version mismatch: {func.__name__}() is only supported at API version {api_version}"
                )
            return func(self, *args, **kwargs)

        return inner

    return wrapper


def token_required(func):
    """Decorator for checking if a user token is provided.

    will raise a ValueError if the user token is not provided
    it expects the first argument to be a user
    """

    @wraps(func)
    def wrapper(self, user: User, *args, **kwargs):
        if user.token is None:
            raise ValueError("A user token is required.")
        return func(self, user, *args, **kwargs)

    return wrapper
