"""
This module defines constants used throughout the Game Jolt API wrapper.

These constants include the base URL for the API, the current API version, 
and a dictionary mapping supported version strings to their respective integer values.
"""

BASE_URL = "https://api.gamejolt.com/api/game/"
API_VERSION = "v1_2"

VERSIONS = {"v1": 1, "v1_1": 2, "v1_2": 3}
