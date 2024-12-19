"""
This subcomponents package provides various components for interacting with the Game Jolt API.

every endpoint has it's own subcomponent
example: `UsersComponent` for `/users/` which is responsible for handling user-related operations.
"""

from .users import UsersComponent
from .data_store import DataStoreComponent
from .trophies import TrophiesComponent
from .sessions import SessionsComponent

__all__ = [
    "UsersComponent",
    "DataStoreComponent",
    "TrophiesComponent",
    "SessionsComponent",
]
