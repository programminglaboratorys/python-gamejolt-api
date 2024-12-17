"""Game Jolt API errors."""

from .models import Response, User


class ApiError(Exception):
    """Base class for exceptions raised by the Game Jolt API."""

    def __init__(self, message, response: Response) -> None:
        super().__init__(message)
        self.response = response


class TrophiesErrors(ApiError):
    """Base class for trophies errors."""

    def __init__(
        self,
        message,
        *,
        trophy_id: int | str = None,
        user: User = None,
        response: Response = None
    ) -> None:
        super().__init__(message, response)
        self.trophy_id = trophy_id
        self.user = user


class IncorrectTrophyID(TrophiesErrors):
    """Raised when the provided trophy ID is incorrect or doesn't belong to current game."""


class UserAlreadyHasTrophy(TrophiesErrors):
    """Raised when the user already has the specified trophy."""


class UserHasNotAchievedTrophy(TrophiesErrors):
    """Raised when the user has not achieved the specified trophy."""
