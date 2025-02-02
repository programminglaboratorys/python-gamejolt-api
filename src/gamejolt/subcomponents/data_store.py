"""This module provides the Data Store component for interacting with the Game Jolt API."""

from typing import overload
from ..models import User
from .component import Component

from .helpers import token_required, api_version_guard, VERSIONS


class DataStoreComponent(Component):
    """
    Data Store Component

    This component handles fetching, setting, removing, updating and getting keys from the Game Jolt API.
    """

    def __user_or_key_checker(
        self, user_or_key: User | str, key_value: str, key_name: str
    ) -> dict[str, str]:
        params = {key_name: key_value}

        if isinstance(user_or_key, User):
            user: User = user_or_key  # assist for the reader
            params["username"] = user.username
            params["user_token"] = user.token

            if user.token is None:
                raise ValueError("User must have a token set.")
        else:
            params[key_name] = user_or_key

        if params[key_name] is None:
            raise ValueError(f"{key_name.capitalize()} must be provided.")
        return params

    @overload
    def fetch(self, key: str) -> str: ...

    @overload
    @token_required
    def fetch(self, user: User, key: str) -> str: ...

    def fetch(self, user_or_key: User | str, key: str = None) -> str:
        """
        Fetches data from the data store.

        :param user_or_key: The user to fetch the data for or the key of the data item to fetch.
        :type user_or_key: User | str
        :param key: The key of the data item to fetch. if only user_or_key is a User, otherwise it gets used
        :type key: str
        :return: The data item as a string.
        :rtype: str
        """

        params = self.__user_or_key_checker(user_or_key, key, "key")

        return self.requester.post(self.requester.DATASTORE.FETCH(**params))

    @overload
    @token_required
    def set(self, user: User, key: str, data: str):
        """
        Sets data in the data store for a user.

        :param user: The user to set the data for.
        :type user: User
        :param key: The key of the data item to set.
        :type key: str
        :param data: The data to set.
        :type data: str
        """

    @overload
    def set(self, key: str, data: str):
        """
        Sets data in the data store globally.

        :param key: The key of the data item to set.
        :type key: str
        :param data: The data to set.
        :type data: str
        """

    def set(self, user_or_key: User | str, key_or_data: str, data: str = None):
        """
        Sets data in the data store.

        :param user_or_key: The user to set the data for or the key of the data item to set.
        :type user_or_key: User | str
        :param key_or_data: If user_or_key is a User, this is the key of the data item to set. Otherwise, it is the data.
        :type key_or_data: str
        :param data: If user_or_key is a User, this is the data to set.
        :type data: str
        """
        params = self.__user_or_key_checker(user_or_key, key_or_data, "key")

        if isinstance(
            user_or_key, User
        ):  # that means key_or_data is key, and user_or_key is user, and data is data
            params["data"] = data
        else:  # otherwise key_or_data is data and user_or_key is key
            params["data"] = key_or_data

        self.requester.post(self.requester.DATASTORE.SET(**params))

    @overload
    def update(self, key: str, operation: str, value: str | int): ...

    @overload
    def update(self, user: User, key: str, operation: str, value: str | int): ...

    def update(self, user_or_key: User | str, operation_or_key: str, *args):
        # key: str, operation: str, value: str | int
        # user: User, key: str, operation: str, value: str | int

        """
        Updates data in the data store.

        :param user_or_key: The user to update the data for or key of the data item to update.
        :type user_or_key: User | str
        :param operation_or_key: If user_or_key is a User, this is the key of the data item to update. Otherwise, it is the operation.
        :type operation_or_key: str
        :param value: If user_or_key is a User, this is the value to apply to the data item. Otherwise, it is the operation.
        :type value: str
        """

        params = self.__user_or_key_checker(user_or_key, operation_or_key, "key")

        if isinstance(user_or_key, User):
            operation, value = args
            params["operation"] = operation
            params["value"] = value
        else:
            value, *_ = args
            params["operation"] = operation_or_key
            params["value"] = value

        return self.requester.post(self.requester.DATASTORE.UPDATE(**params))

    @overload
    def remove(self, key: str):
        """
        Removes data from the data store globally.

        :param key: The key of the data item to remove.
        :type key: str
        """

    @overload
    @token_required
    def remove(self, user: User, key: str):
        """
        Removes data from the data store.

        :param user: The user to remove the data for.
        :type user: User
        :param key: The key of the data item to remove.
        :type key: str
        """

    def remove(self, user_or_key: User | str, key: str = None):
        """
        Removes data from the data store.

        :param user_or_key: The user to remove the data for or key of the data item to remove.
        :type user_or_key: User | str
        :param key: The key of the data item to remove. used if user_or_key is a User
        :type key: str
        """

        params = self.__user_or_key_checker(user_or_key, key, "key")

        return self.requester.post(self.requester.DATASTORE.REMOVE(**params))

    @overload
    def get_keys(self, pattern: str) -> list[dict[str, str]] | str: ...

    @overload
    @api_version_guard("v1_2")
    @token_required
    def get_keys(
        self, user: User, pattern: str = None
    ) -> list[dict[str, str]] | str: ...

    @overload
    @token_required
    def get_keys(self, user: User) -> list[dict[str, str]] | str: ...

    def get_keys(
        self, user_or_pattern: User | str, pattern: str = None
    ) -> list[dict[str, str]] | str:
        """
        Gets a list of keys from the data store.

        :param user_or_pattern: The user to get the keys for. If None, gets globally.
        :type user_or_pattern: User
        :param pattern: The pattern to apply to the key names in the data store.
        :type pattern: str
        :return: A list of keys from the data store.
        :rtype: list[dict[str, str]] | str

        return a string if there is no keys or a list of dictionaries
        example: [{"key":"test"},{"key":"version"}]

        """
        params = self.__user_or_key_checker(user_or_pattern, pattern, "pattern")
        if isinstance(user_or_pattern, User):
            params["pattern"] = pattern
        if (
            params["pattern"] is not None
            and VERSIONS[self.requester.api_version] < VERSIONS["v1_2"]
        ):
            raise ValueError(
                "API version mismatch: pattern argument is only supported at API version v1_2"
            )

        return self.requester.post(self.requester.DATASTORE.GET_KEYS(**params)).keys
