from dataclasses import dataclass, field
from . import GenericModel


@dataclass
class Response(GenericModel):
    """
    Represents a response from the Game Jolt API.

    :var success: Whether the request was successful or not.
    :vartype success: bool
    :var response: The response of the request.
    :vartype response: dict
    :var message: The error message if the request was not successful (default: None).
    :vartype message: str | None
    """

    success: bool
    response: dict = field(repr=False)
    message: str | None = field(default=None)
