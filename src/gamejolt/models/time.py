"""
This module defines the Time model for representing time within the Game Jolt API.
"""

from dataclasses import dataclass, field
from datetime import datetime
from . import GenericModel


@dataclass
class Time(GenericModel):
    """
    Represents Time

    This model represents time in the Game Jolt API. It inherits from the GenericModel

    Attributes
    ----------
        timestamp (int): The UNIX time stamp (in seconds) representing the server's time.
        timezone (str): The timezone of the server.
        year (int): The current year.
        month (int): The current month.
        day (int): The day of the month.
        hour (int): The hour of the day.
        minute (int): The minute of the hour.
        second (int): The seconds of the minute.
    """

    timestamp: int = field(repr=False)
    timezone: str
    year: int
    month: int
    day: int
    hour: int
    minute: int
    second: int

    @property
    def datetime(self) -> datetime:
        """Returns the datetime object from the timestamp"""
        return datetime.fromtimestamp(self.timestamp)
