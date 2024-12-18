"""This module provides the Sessions component for interacting with the Game Jolt API."""

from ..models import User
from ..errors import ApiError
from .component import Component
from .helpers import token_required, api_version_guard


class SessionsComponent(Component):
    """
    Sessions Component

    This component handles opening, pinging, checking and closing sessions from the Game Jolt API.
    """

    @token_required
    def open(self, user: User) -> bool:
        """
        Opens a session.

        :param user: The user to open the session for.
        :type user: User
        :return: boolean indicating whether the session was opened.
        :rtype: bool
        """
        return self.requester.post(
            self.requester.SESSIONS.OPEN(username=user.username, user_token=user.token)
        ).success

    @token_required
    def ping(self, user: User) -> bool:
        """
        Pings a session.

        :param user: The user to ping the session for.
        :type user: User
        :return: boolean indicating whether the session was pinged.
        :rtype: bool
        """
        return self.requester.post(
            self.requester.SESSIONS.PING(username=user.username, user_token=user.token)
        ).success

    @api_version_guard("v1_2")
    @token_required
    def check(self, user: User) -> bool:
        """
        Checks if a session is open.

        :param user: The user to check the session for.
        :type user: User
        :return: A boolean indicating whether the session is open.
        :rtype: bool
        """
        try:
            return self.requester.post(
                self.requester.SESSIONS.CHECK(
                    username=user.username, user_token=user.token
                )
            ).success
        except ApiError as e:
            if e.response.message is not None:
                raise e from None
            return False

    @token_required
    def close(self, user: User) -> bool:
        """
        Closes a session.

        :param user: The user to close the session for.
        :type user: User
        :return: A boolean indicating whether the session was closed successfully.
        :rtype: bool
        """
        return self.requester.post(
            self.requester.SESSIONS.CLOSE(username=user.username, user_token=user.token)
        ).success
