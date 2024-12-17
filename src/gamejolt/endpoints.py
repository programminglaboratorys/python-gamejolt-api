from urllib.parse import urlencode
from .utils import AttrDict

BASE_URL = "https://api.gamejolt.com/api/game/"
API_VERSION = "v1_2"

supported_formats = ["json", "keypair", "dump", "xml"]  # gamejolt supported formats

Endpoints = AttrDict(
    USERS=AttrDict(FETCH="/users", AUTH="/users/auth"),
    SESSIONS=AttrDict(
        OPEN="/sessions/open",
        PING="/sessions/ping",
        CHECK="/sessions/check",
        CLOSE="/sessions/close",
    ),
    SCORES=AttrDict(
        FETCH="/scores/",
        ADD="/scores/add",
        GET_RANK="/scores/get-rank",
        TABLES="/scores/tables",
    ),
    TROPHIES=AttrDict(
        FETCH="/trophies",
        ADD_ACHIEVED="/trophies/add-achieved",
        REMOVE_ACHIEVED="/trophies/remove-achieved",
    ),
    DATASTORE=AttrDict(
        FETCH="/data-store/fetch",
        GET_KEYS="/data-store/get-keys",
        REMOVE="/data-store/remove",
        SET="/data-store/set",
        UPDATE="/data-store/update",
    ),
    FRIENDS=AttrDict(FETCH="/friends"),
    TIME=AttrDict(FETCH="/time"),
)


def format_queries(url: str = "", /, encoding: str = "utf-8", **queries):
    """
    Formats the given URL with query parameters.

    :param url: The base URL to which the queries will be appended.
    :param encoding: The encoding to use for the query parameters. Defaults to "utf-8".
    :param queries: The query parameters to be appended to the URL.
    :return: The formatted URL with query parameters.
    :rtype: str
    """
    return ((url and url + "?") or "") + urlencode(queries, encoding=encoding)


class FormatterAbstract(object):
    """
    Abstract base class for formatting API endpoints.

    This class provides a basic interface for formatting URLs from API endpoints and query parameters.

    Attributes
    ----------
        base_url (str): The base URL of the Game Jolt API.
        api_version (str): The version of the Game Jolt API.
        queries (dict[str, str]): A dictionary of additional query parameters to be included in the request.

    Methods
    -------
        format(url: str = "", /, encoding: str = "utf-8", **queries) -> str:
            Formats the given URL with query parameters.
        format_url(endpoint: str = "") -> str:
            Formats the complete URL by appending the API version and endpoint to the base URL.
    """

    def __init__(self, *, base=BASE_URL, version=API_VERSION, **kwargs):
        self.base_url = base
        self.api_version = version
        self.queries = kwargs

    def format_url(self, endpoint: str = "") -> str:
        """
        Formats the complete URL by appending the API version and endpoint to the base URL.

        :param endpoint: The specific endpoint path to append to the base URL. (optional)
        :type endpoint: str
        :return: The fully formatted URL string.
        :rtype: str

        This method constructs a URL by combining the base URL, API version, and a specified endpoint.
        When an endpoint is provided, it is appended to the base URL and version, forming a complete URL.
        """

        return f"{self.base_url}{self.api_version}{endpoint}"

    def format_queries(
        self, /, url: str = "", encoding: str = "utf-8", **queries: dict[str, str]
    ) -> str:
        """
        Formats the given URL with query parameters.

        :param url: The base URL to which the queries will be appended.
        :type url: str
        :param queries: Additional query parameters to append to the URL. These are merged with the instance's queries.
        :type queries: dict
        :return: The formatted URL with query parameters.
        :rtype: str

        The function combines the provided queries with the instance's queries. It encodes
        the keys and values using `quote_plus` to ensure they are URL-safe. The resulting
        query string is appended to the URL, separating the base URL and the query parameters
        with a '?' and joining multiple parameters with '&'.
        """
        return format_queries(url, encoding, **(self.queries | queries))

    def format(self, endpoint: str = "", **queries: dict[str, str]) -> str:
        """
        Formats the complete URL by appending the API version, endpoint, and query parameters to the base URL.

        :param endpoint: The specific endpoint path to append to the base URL. (optional)
        :type endpoint: str
        :param queries: Additional query parameters to append to the URL. These are merged with the instance's queries.
        :type queries: dict
        :return: The fully formatted URL string.
        :rtype: str
        """
        return self.format_queries(self.format_url(endpoint), **queries)


class Formatter(FormatterAbstract):
    """
    Concrete implementation of the FormatterAbstract class.

    This class provides a basic interface for formatting URLs from API endpoints and query parameters.
    It is the primary class for formatting URLs and is instantiated with the base URL and API version.
    """

    def __getattr__(self, key):
        """
        Returns an attribute of the current instance, or an EndpointWrapper if key exists in the constant Endpoints.

        :param key: The name of the attribute to retrieve.
        :type key: str
        :return: The value of the attribute if it exists.
        :raises AttributeError: If the attribute does not exist.
        """
        if key in Endpoints:
            return EndpointWrapper(self, Endpoints[key])
        if hasattr(super(), "__getattr__"):
            return super().__getattr__(key)
        raise AttributeError(
            f"type object '{type(self).__name__}' has no attribute '{key}'"
        )


class EndpointWrapper(AttrDict):
    """
    Wraps an Endpoint dictionary, providing a convenient way to access and format the URLs.

    :param formatter: The Formatter instance to use for formatting URLs.
    :type formatter: Formatter
    :param endpoints: The dictionary of endpoints to wrap.
    :type endpoints: AttrDict[str, str]
    """

    __slots__ = (
        "formatter",
        "endpoints",
    )

    def __init__(self, formatter: Formatter, endpoints: AttrDict[str, str]):
        self.endpoints = endpoints
        self.formatter = formatter

    def __dir__(self):
        return dir(type(self)) + list(self.endpoints)

    def __getattr__(self, key):
        if key in self.__slots__:
            return super().__getattr__(key)
        if key in self.endpoints:
            # maybe add repr in the future
            return lambda *args, **kwargs: self.formatter.format(
                self.endpoints[key], *args, **kwargs
            )
        if hasattr(super(), "__getattr__"):
            return super().__getattr__(key)
        raise AttributeError(
            f"type object '{type(self).__name__}' has no attribute '{key}'"
        )
