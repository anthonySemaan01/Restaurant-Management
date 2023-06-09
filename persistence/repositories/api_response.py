from typing import Any


class ApiResponse:
    def __init__(self, success: bool = True, data: Any = None, error=None):
        """
        Defines the response shape
        :param success: A boolean that returns if the request has succeeded or not
        :param data: The model's response
        :param error: The error in case an exception was raised
        """
        self.data: Any = data
        self.error: Exception = error.__str__() if error is not None else ''
        self.success: bool = success
