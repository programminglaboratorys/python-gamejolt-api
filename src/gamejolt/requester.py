"""
This module provides functionality for interacting with the Game Jolt API.

It includes the ability to generate request signatures using a private key,
append those signatures to URLs, and handle HTTP POST requests to the API.
Additionally, the module offers tools for formatting URLs with query
parameters, and evaluating the responses of API requests.

Classes:
    RequesterAbstract: An abstract base class for making requests to the Game Jolt API.
    Response: Represents a response from a request to the Game Jolt API.

Functions:
    generate_signature(url: str, key: str) -> str: Generates a signature for a URL and key.
"""

import hashlib

from .endpoints import Formatter, format_queries, supported_formats
from .models import Response
from .errors import ApiError


def generate_signature(url: str, key: str) -> str:
    """
    Generates the signature for the provided URL and key.

    :param url: The URL of the request
    :type url: str
    :param key: The private key to be used for generating the signature.
    :type key: str
    :return: The generated signature.
    :rtype: str
    """
    return hashlib.md5((url + key).encode("ascii")).hexdigest()


class RequesterAbstract(Formatter):
    """
    Abstract base class for making requests to the Game Jolt API.

    This class will automatically generate the signature for the request and
    append it to the URL. It also provides a method for evaluating the response
    of the request.

    Attributes
    -----------
        private_key (str): The private key to be used for generating request
            signatures.
        game (int or str): The game ID to be included in requests. Can be an
            integer or string.
        format (str): The format of the request. Defaults to 'json'.
        base_url (str): The base URL of the Game Jolt API.
        api_version (str): The version of the Game Jolt API.
        queries (dict[str, str]): A dictionary of additional query parameters to
            be included in the request.
    """

    def generate_signature(self, url: str) -> str:
        """
        Generates the signature for the provided URL and key.

        :param url: The URL of the request
        :type url: str
        :return: The generated signature.
        :rtype: str
        """
        return generate_signature(url, self.private_key)

    def __init__(
        self, key: str, *, game: int | str, response_format: str = "json", **kwargs
    ):
        """
        Initializes a new instance of the Requester class.

        :param key: The private key to be used for generating request signatures.
        :type key: str
        :param game: The game ID to be included in requests. Can be an integer or string.
        :type game: int or str
        :param response_format: The format of the response. Defaults to "json".
        :type response_format: str
        :param kwargs: Additional keyword arguments to be passed to the parent class initializer.
        :type kwargs: dict

        Initializes the Requester with the specified private key, game ID, and response format.
        It also sets up any additional query parameters provided through kwargs.
        """
        if response_format not in supported_formats:
            raise ValueError(
                f"Invalid response format: {response_format}. "
                f"Supported formats are: {', '.join(supported_formats)}"
            )
        super().__init__(game_id=game, format=response_format, **kwargs)
        self.private_key = key

    def format_signature(self, url: str) -> str:
        """
        Appends the signature to the url.
        the function expects the url to be already formatted with query parameters
        otherwise you will get an invalid url

        :param url: The url to append the signature to.
        :return: The url with the signature appended.
        """
        return "&".join((url, format_queries(signature=self.generate_signature(url))))

    def format(self, endpoint: str = "", **queries: dict[str, str]) -> str:
        """
        Appends the signature to the url.
        the function expects the url to be already formatted with query parameters
        otherwise you will get an invalid url

        :param endpoint: The endpoint to append the signature to.
        :type endpoint: str
        :param queries: The query parameters to append to the endpoint.
        :type queries: dict[str, str]
        :return: The url with the signature appended.
        """
        return self.format_signature(super().format(endpoint, **queries))

    def post(self, url: str) -> Response:
        """
        Makes a POST request to the provided url.

        :param url: The url to make the request to.
        :return: A Response object containing the result of the request.
        :rtype: Response

        :raise ApiError: If the request was not successful.
        """
        response = self._post(url)
        evaled_response = self.evaluate(response)
        response_model = Response.from_dict(evaled_response)
        if not evaled_response["success"]:
            raise ApiError(evaled_response["message"], response=response_model)
        return response_model

    def _post(self, url: str) -> any:
        """
        Makes a POST request to the provided url.

        :param url: The url to make the request to.
        :return: The response of the request.
        :rtype: any
        """
        raise NotImplementedError()

    def evaluate(self, response: any) -> dict:
        """
        Parses the response of the request.

        The expected output is a dict with two keys:
            - success: bool
            - response: dict
            - message?: str

        The success key determines if the request was a success or not.
        The response key contains the rest of the response.
        The message key contains the error message if the request was not successful.

        :param response: The response of the request.
        :type response: any
        :return: The parsed response.
        :rtype: dict
        """
        raise NotImplementedError()
