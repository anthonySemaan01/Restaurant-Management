import datetime

from pydantic import BaseModel
from datetime import date


class StaffSignUpRequest(BaseModel):
    first_name: str
    last_name: str
    email: str
    password: str
    phone_nb: str
    date_of_birth: date = datetime.date.today()


class StaffUploadImage(BaseModel):
    id: int


def staff_sign_up_request_validator(user_sign_up_request: StaffSignUpRequest):
    if len(user_sign_up_request.first_name) < 3:
        raise ValueError()
