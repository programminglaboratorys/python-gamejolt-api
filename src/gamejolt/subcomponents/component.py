"""This module provides the Generic component for all subcomponents."""

from .. import RequesterAbstract


# pylint: disable=too-few-public-methods
class Component:
    """
    Generic Component
    """

    def __init__(self, requester: RequesterAbstract) -> None:
        self.requester = requester
