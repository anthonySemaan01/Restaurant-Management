import datetime
from datetime import date

from pydantic import BaseModel


class UserSignUpRequest(BaseModel):
    first_name: str
    last_name: str
    email: str
    password: str
    phone_nb: str
    date_of_birth: date = datetime.date.today()


class UserUploadImage(BaseModel):
    id: int


def users_sign_up_request_validator(user_sign_up_request: UserSignUpRequest):
    if len(user_sign_up_request.first_name) < 3:
        raise ValueError()
