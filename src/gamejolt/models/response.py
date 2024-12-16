from dataclasses import dataclass

@dataclass
class Response:
    """
    Represents a response from a request to the Game Jolt API.

    :var success: Whether the request was successful or not.
    :vartype success: bool
    :var response: The response of the request.
    :vartype response: dict
    """
    success: bool
    response: dict
    