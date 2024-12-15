from utils import AttrDict # temporary

BASE_URL = "https://api.gamejolt.com/api/game"
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

class Formatter(object):
    def __init__(self, **kwargs):
        self.queries = kwargs
