from utils import AttrDict # temporary
from urllib.parse import urlencode # temporary

BASE_URL = "https://api.gamejolt.com/api/game/"
API_VERSION = "v1_2"

supported_formats = [ # gamejolt supported formats
    "json",
    "keypair",
    "dump",
    "xml"
]

Endpoints = AttrDict(
    USERS = AttrDict(
        FETCH = "/users",
        AUTH = "/users/auth"
    ),
    SESSIONS = AttrDict(
        OPEN = "/sessions/open",
        PING = "/sessions/ping",
        CHECK = "/sessions/check",
        CLOSE = "/sessions/close"
    ),
    SCORES = AttrDict(
        FETCH = "/scores/",
        ADD = "/scores/add",
        GET_RANK = "/scores/get-rank",
        TABLES = "/scores/tables"
    ),
    TROPHIES = AttrDict(
        FETCH = "/trophies",
        ADD_ACHIEVED = "/trophies/add-achieved",
        REMOVE_ACHIEVED = "/trophies/remove-achieved"
    ),
    DATASTORE = AttrDict(
        FETCH = "/data-store/fetch",
        GET_KEYS = "/data-store/get-keys",
        REMOVE = "/data-store/remove",
        SET = "/data-store/set",
        UPDATE = "/data-store/update"
    ),
    FRIENDS = AttrDict(
        FETCH = "/friends"
    ),
    TIME = AttrDict(
        FETCH = "/time"
    )
)

def format_queries(url: str, /, encoding: str="utf-8", **queries):
    return url+"?"+urlencode(queries, encoding=encoding)

class FormatterAbstract(object):
    def __init__(self, *, base=BASE_URL, version=API_VERSION, **kwargs):
        self.BASE_URL = base
        self.API_VERSION = version
        self.queries = kwargs
    
    def format_url(self, endpoint: str="") -> str:
        """
        Formats the complete URL by appending the API version and endpoint to the base URL.

        :param endpoint: The specific endpoint path to append to the base URL. (optional)
        :type endpoint: str
        :return: The fully formatted URL string.
        :rtype: str

        This method constructs a URL by combining the base URL, API version, and a specified endpoint.
        When an endpoint is provided, it is appended to the base URL and version, forming a complete URL.
        """

        return f"{self.BASE_URL}{self.API_VERSION}{endpoint}"

    def format_queries(self, /, url: str, encoding: str="utf-8", **queries: dict[str, str]) -> str:
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
        return format_queries(url, encoding, **(self.queries|queries))
    
    def format(self, endpoint: str="", **queries: dict[str, str]) -> str:
        return self.format_queries(self.format_url(endpoint), **queries)



class Formatter(FormatterAbstract):
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
        return super().__getattr__(key)


class EndpointWrapper(AttrDict):
    __slots__ = ("formatter",'endpoints',)
    def __init__(self, formatter: Formatter, endpoints: AttrDict[str, str]):
        self.endpoints = endpoints
        self.formatter = formatter
    
    def __dir__(self):
        return dir(type(self))+list(self.endpoints)
    
    def __getattr__(self, key):
        if key in self.__slots__:
            return super().__getattr__(key)
        if key in self.endpoints:
            # maybe add repr in the future
            return lambda *args, **kwargs: self.formatter.format(self.endpoints[key], *args, **kwargs)
        return super().__getattr__(key)
