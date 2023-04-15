from pydantic import BaseModel


class StaffSignInRequest(BaseModel):
    email: str
    password: str
