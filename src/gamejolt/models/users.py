"""
This module defines the User model for representing users within the Game Jolt API.
"""

from dataclasses import dataclass, field
from . import GenericModel


@dataclass
class User(GenericModel):
    """
    Represents User

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
    avatar_url: str = field(repr=False)
    signed_up: str
    signed_up_timestamp: int = field(repr=False)
    last_logged_in: str
    last_logged_in_timestamp: int = field(repr=False)
    status: str
    developer_name: str | None = field(default=None, repr=False)
    developer_website: str | None = field(default=None, repr=False)
    developer_description: str | None = field(default=None, repr=False)
    token: str | None = field(default=None, repr=False)

    def __post_init__(self):
        self.id = int(self.id)

    def set_token(self, token: str):
        """Sets the token of the user.

        :param token: The token to set.
        :type token: str
        """
        self.token = token
