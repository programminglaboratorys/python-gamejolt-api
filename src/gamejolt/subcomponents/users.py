"""This module provides the Users component for interacting with the Game Jolt API."""

from typing import overload

from .helpers import instance_checker
from ..models import User, Response
from .component import Component


class UsersComponent(Component):
    """
    Users Component

    This component handles fetching users from the Game Jolt API.
    """

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

    def fetch(self, *users: int | str) -> list[User] | User:
        """
        Fetches one or more users.

        :param users: The id or username of the user to be fetched.
        :type users: int | str
        :return: A list of User instances if multiple users where passed, otherwise a single User instance.
        :rtype: list[User] | User

        :raises TypeError: If the iterable contains a mix of integers and strings.
        """
        if instance_checker(int, users) and instance_checker(str, users):
            raise TypeError("the iterable should be an array of intagers only")

        if instance_checker(int, users):
            url = self.requester.USERS.FETCH(user_id=",".join(map(str, users)))
        else:
            url = self.requester.USERS.FETCH(username="".join(users))
        rp = self.requester.post(url)
        if len(users) == 1:
            return User.from_dict(rp.response["users"][0])
        return User.from_list(rp.response["users"])

    def authenticate(self, username: str, token: str) -> Response:
        """
        Authenticate a user.

        :param username: The username of the user to be authenticated.
        :type username: str
        :param token: The token of the user to be authenticated.
        :type token: str
        """
        return self.requester.post(
            self.requester.USERS.AUTH(username=username, user_token=token)
        )
