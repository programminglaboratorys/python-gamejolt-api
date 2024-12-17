"""Generic dataclass for arbitrary data."""
import inspect
from dataclasses import dataclass

@dataclass
class GenericModel:
    """
    A dataclass that can be used to model arbitrary data.

    This class is a generic dataclass that can be used to model any data. It has
    a single method, `from_dict`, that can be used to create an instance from a
    dictionary.

    Attributes:
        All attributes are determined by the dictionary passed to the `from_dict`
        method. The attribute names are the keys of the dictionary, and the
        attribute values are the values of the dictionary.
    """
    @classmethod
    def from_dict(cls, data: dict):
        """
        Creates an instance of the class from a dictionary.

        :param data: A dictionary containing the data to initialize the class instance.
        :type data: dict
        :return: An instance of the class initialized with the provided dictionary data.
        :rtype: GenericModel
        """
        return cls(**{
            k: v for k, v in data.items() 
            if k in inspect.signature(cls).parameters
        })
