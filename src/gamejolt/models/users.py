"""
This module defines the User model for representing users within the Game Jolt API.
"""

from dataclasses import dataclass
from . import GenericModel


@dataclass
class User(GenericModel):
    """
    User Model

    This model represents a user in the Game Jolt API. It inherits from the GenericModel

    Attributes
    ----------
        id (int): The ID of the user.
        type (str): The type of user. Can be User, Developer, Moderator, or Administrator.
        username (str): The user's username.
        avatar_url (str): The URL of the user's avatar.
        signed_up (str): How long ago the user signed up.
        signed_up_timestamp (int): The timestamp (in seconds) of when the user signed up.
        last_logged_in (str): How long ago the user was last logged in. Will be Online Now if the user is currently online.
        last_logged_in_timestamp (int): The timestamp (in seconds) of when the user was last logged in.
        status (str): Active if the user is still a member of the site. Banned if they've been banned.
        developer_name (str): The user's display name.
        developer_website (str): The user's website (or empty string if not specified)
        developer_description (str): The user's profile markdown description.
    """

    id: int
    type: str
    username: str
    avatar_url: str
    signed_up: str
    signed_up_timestamp: int
    last_logged_in: str
    last_logged_in_timestamp: int
    status: str
    developer_name: str
    developer_website: str
    developer_description: str

    @classmethod
    def from_list(cls, data: list[dict]) -> list["User"]:
        """
        Creates a list of instances from a list of dictionaries.

        :param data: A list of dictionaries containing the data to initialize the class instances.
        :type data: list[dict]
        :return: A list of instances of the class initialized with the provided dictionary data.
        :rtype: list[User]
        """
        return [cls.from_dict(data) for data in data]

    def __post_init__(self):
        self.id = int(self.id)
