from domain.exceptions.application_error import ApplicationError


class AddRestaurantException(ApplicationError):
    """"
    raised when an error occur while trying to access the DB"""

    def __init__(self, additional_message: str):
        super().__init__(default_message="An Error Occurred While adding a restaurant",
                         additional_message=additional_message)
