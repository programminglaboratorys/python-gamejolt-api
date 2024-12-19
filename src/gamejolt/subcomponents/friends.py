"""This module provides the Friends component for interacting with the Game Jolt API."""

from ..models import User
from .component import Component
from .helpers import api_version_guard, token_required


class FriendsComponent(Component):
    """
    Friends Component

    This component handles fetching friends from the Game Jolt API.
    """

    @api_version_guard("v1_2")
    @token_required
    def fetch(self, user: User) -> list[User]:
        """
        Fetches friends for the specified user.

        :param user: The user to fetch friends for.
        :type user: User
        :return: A list of friends ids.
        :rtype: list[dict[str, str]]

        example: [{"friend_id":"12345"}]
        """
        response = self.requester.post(
            self.requester.FRIENDS.FETCH(user_token=user.token, username=user.username)
        )
        return response.response["friends"]
