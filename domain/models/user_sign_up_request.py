import datetime

from pydantic import BaseModel
from typing import List, Optional
from fastapi import UploadFile
from datetime import date


class UserSignUpRequest(BaseModel):
    email: str
    password: str
    phone_nb: str
    first_name: str
    last_name: str
    date_of_birth: date = datetime.date.today()
    picture: Optional[UploadFile]
