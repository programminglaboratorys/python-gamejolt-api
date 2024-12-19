"""
This package contains models for representing data from the Game Jolt API.

This package provides models for representing data from the Game Jolt API. It
includes models for representing users, trophies, scores, and other data that
can be retrieved from the Game Jolt API.

"""

from .generic_model import GenericModel
from .response import Response
from .users import User
from .trophies import Trophy


__all__ = ["Response", "GenericModel", "User", "Trophy"]
