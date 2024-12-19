"""This module provides the Time component for interacting with the Game Jolt API."""

from ..models import Time
from .component import Component
from .helpers import api_version_guard


class TimeComponent(Component):
    """
    Time Component

    This component handles fetching the current time from the Game Jolt API.
    """

    @api_version_guard("v1_2")
    def fetch(self) -> Time:
        """
        Fetches the current time from the Game Jolt API.

        :return: A Time instance containing the time.
        :rtype: Time
        """
        return Time.from_dict(self.requester.post(self.requester.TIME.FETCH()).response)
