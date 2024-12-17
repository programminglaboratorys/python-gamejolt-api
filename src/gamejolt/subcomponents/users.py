"""This module provides the Users component for interacting with the Game Jolt API."""

from typing import overload, Iterable

from ..models import User
from .. import RequesterAbstract


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


class UsersComponent:
    """
    Users Component

    This component handles fetching users from the Game Jolt API.
    """

    def __init__(self, requester: RequesterAbstract) -> None:
        self.requester = requester

    def fetch(self, id_or_username: int | str, *ids: int) -> list[User] | User:
        """
        Fetches one or more users.

        :param id_or_username: The id or username of the user to be fetched.
        :type id_or_username: int | str
        :param ids: Additional ids of the users to be fetched.
        :type ids: int
        :return: A list of User instances if multiple users where passed, otherwise a single User instance.
        :rtype: list[User] | User

        :raises TypeError: If the iterable contains a mix of integers and strings.
        """
        users = [id_or_username, *ids]
        if ids and instance_checker(int, users) and instance_checker(str, users):
            raise TypeError("the iterable should be an array of intagers only")

        if instance_checker(int, users):
            url = self.requester.USERS.FETCH(user_id=",".join(map(str, users)))
        else:
            url = self.requester.USERS.FETCH(username="".join(users))
        rp = self.requester.post(url)
        if len(users) == 1:
            return User(**rp.response["users"][0])
        return [User(**user) for user in rp.response["users"]]

    @overload
    def fetch(self, id: int) -> User:
        """
        Fetches a user.

        :param id: The id of the user to be fetched.
        :type id: int
        :return: A User instance.
        :rtype: User
        """

    @overload
    def fetch(self, username: str) -> User:
        """
        Fetches a user.

        :param username: The username of the user to be fetched.
        :type username: str
        :return: A User instance.
        :rtype: User
        """

    @overload
    def fetch(self, *ids: int) -> list[User]:
        """
        Fetches multiple users.

        :param ids: The ids of the users to be fetched.
        :type ids: int
        :return: A list of User instances.
        :rtype: list[User]
        """

    def authenticate(self, username: str, token: str):
        """
        Authenticate a user.

        :param username: The username of the user to be authenticated.
        :type username: str
        :param token: The token of the user to be authenticated.
        :type token: str
        :return: A User instance.
        :rtype: User
        """
        return self.requester.post(
            self.requester.USERS.AUTH(username=username, user_token=token)
        )
