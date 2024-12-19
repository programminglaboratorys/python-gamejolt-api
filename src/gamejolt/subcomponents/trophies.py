"""This module provides the Trophies component for interacting with the Game Jolt API."""

from typing import overload, NoReturn
from ..errors import (
    IncorrectTrophyID,
    UserAlreadyHasTrophy,
    UserHasNotAchievedTrophy,
    ApiError,
)

from ..models import User, Trophy, Response
from .component import Component
from .helpers import api_version_guard, token_required


# TODO: add overload for add_achieved, remove_achieved so it can take id as int, or it could take a trophy object
class TrophiesComponent(Component):
    """Trophies Component

    This component handles fetching trophies from the Game Jolt API.
    """

    @overload
    def fetch(self, user: User, *, achieved: bool = None) -> list[Trophy]:
        """Fetches all trophies for the specified user.

        :param user: The user to fetch trophies for.
        :type user: User
        :param achieved: Whether to filter trophies by achieved status. (default: None)
        :type achieved: bool
        :return: A list of Trophy instances.
        :rtype: list[Trophy]
        """

    @overload
    def fetch(self, user: User, trophy_id: int, *, achieved: bool = None) -> Trophy:
        """
        Fetches a specific trophy for the specified user.

        :param user: The user to fetch the trophy for.
        :type user: User
        :param trophy_id: The ID of the trophy to fetch.
        :type trophy_id: int
        :return: A Trophy instance.
        :rtype: Trophy
        """

    # pylint: disable=keyword-arg-before-vararg
    @token_required
    def fetch(
        self, user: User, trophy_id: int = None, *ids: int, **kw
    ) -> list[Trophy] | Trophy:
        """
        either fetches all trophies for the specified user, or a single trophy if trophy_id is given or more positional

        :param user: The user to fetch trophies for.
        :type user: User
        :param trophy_id: The ID of the trophy to fetch. If None, fetches all trophies.
        :type trophy_id: int
        :return: A list of Trophy instances if no trophy_id is given, or a single Trophy if a trophy_id is given.
        :rtype: list[Trophy] | Trophy
        :raises ValueError: If the User does not have a token set.
        """
        url_kwargs = {"username": user.username, "user_token": user.token}
        if trophy_id is not None:
            url_kwargs["trophy_id"] = ",".join(map(str, [trophy_id, *ids]))
        if kw.get("achieved") is not None:
            url_kwargs["achieved"] = kw["achieved"]
        url = self.requester.TROPHIES.FETCH(**url_kwargs)
        response: Response = self.requester.post(url)
        if trophy_id is not None and not ids:
            return Trophy.from_dict(response.response["trophies"][0])
        return Trophy.from_list(response.response["trophies"])

    @token_required
    def add_achieved(self, user: User, trophy_id: int):
        """
        Adds a trophy as achieved for the specified user.

        :param user: The user to add the trophy to.
        :type user: User
        :param trophy_id: The ID of the trophy to add.
        :type trophy_id: int
        :raises UserAlreadyHasTrophy: If the user already has the trophy.
        :raises IncorrectTrophyID: If the trophy ID is invalid.
        """
        url = self.requester.TROPHIES.ADD_ACHIEVED(
            username=user.username, user_token=user.token, trophy_id=trophy_id
        )
        try:
            return self.requester.post(url)
        except ApiError as e:
            self._raise_error(e, trophy_id, user)

    @api_version_guard("v1_2")
    @token_required
    def remove_achieved(self, user: User, trophy_id: int):
        """
        Removes the specified trophy from the user's achieved trophies.

        :param user: The user to remove the trophy from.
        :type user: User
        :param trophy_id: The ID of the trophy to remove.
        :type trophy_id: int
        :raises IncorrectTrophyID: If the trophy ID is invalid.
        :raises UserHasNotAchievedTrophy: If the user does not have the trophy.
        """
        url = self.requester.TROPHIES.REMOVE_ACHIEVED(
            username=user.username, user_token=user.token, trophy_id=trophy_id
        )
        try:
            return self.requester.post(url)
        except ApiError as e:
            self._raise_error(e, trophy_id, user)

    def _raise_error(
        self, error: ApiError, trophy_id: int = None, user: User = None
    ) -> NoReturn:
        """Raises the appropriate error based on the error message.

        :param error: The error to raise.
        :type error: ApiError
        :param trophy_id: The ID of the trophy.
        :type trophy_id: int
        :param user: The user.
        :type user: User
        :raises UserAlreadyHasTrophy: If the user already has the trophy.
        :raises IncorrectTrophyID: If the trophy ID is invalid.
        :raises UserHasNotAchievedTrophy: If the user does not have the trophy.
        """
        response = error.response
        message = response.message
        if message == "The user already has this trophy.":
            raise UserAlreadyHasTrophy(
                f"User {user.username} already has trophy {trophy_id}",
                trophy_id=trophy_id,
                user=user,
                response=response,
            ) from None
        if message == "Incorrect trophy ID.":
            raise IncorrectTrophyID(
                f"Invalid trophy ID: {trophy_id}",
                trophy_id=trophy_id,
                user=user,
                response=response,
            ) from None
        if message == "The user does not have this trophy.":
            raise UserHasNotAchievedTrophy(
                f"User {user.username} does not have trophy {trophy_id}",
                trophy_id=trophy_id,
                user=user,
                response=response,
            ) from None
        raise error from None
