"""
This module defines the Trophy model for representing trophies within the Game Jolt API.
"""

from dataclasses import dataclass
from . import GenericModel


@dataclass
class Trophy(GenericModel):
    """
    Trophy Model

    This model represents a trophy in the Game Jolt API. It inherits from the GenericModel.

    Attributes
    ----------
        id (int): The ID of the trophy.
        title (str): The title of the trophy on the site.
        description (str): The trophy description text.
        difficulty (str): The difficulty of the trophy. Can be Bronze, Silver, Gold, or Platinum.
        image_url (str): The URL of the trophy's thumbnail image.
        achieved (bool or str): Date/time when the trophy was achieved by the user, or False if they haven't achieved it yet.
    """

    id: int
    title: str
    description: str
    difficulty: str
    image_url: str
    achieved: bool | str

    def __post_init__(self):
        self.id = int(self.id)
