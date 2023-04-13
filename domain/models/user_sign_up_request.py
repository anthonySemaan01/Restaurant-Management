import datetime

from pydantic import BaseModel
from typing import List, Optional
from fastapi import UploadFile
from datetime import date


class UserSignUpRequest(BaseModel):
    first_name: str
    last_name: str
    email: str
    password: str
    phone_nb: str
    date_of_birth: date = datetime.date.today()
    picture: Optional[UploadFile]

def users_sign_up_request_validator(user_sign_up_request: UserSignUpRequest):
    if len(user_sign_up_request.first_name) < 3:
        raise ValueError()