from domain.exceptions.application_error import ApplicationError


class UserSignUpException(ApplicationError):
    """"
    raised when an error occur while trying to access the DB"""

    def __init__(self, additional_message: str):
        super().__init__(default_message="An Error Occurred While SignUp", additional_message=additional_message)


class UserSignInException(ApplicationError):
    """"
    raised when an error occur while trying to access the DB"""

    def __init__(self, additional_message: str):
        super().__init__(default_message="An Error Occurred While SignIn", additional_message=additional_message)



