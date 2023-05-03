from pydantic import BaseModel


class AssignManagerRequest(BaseModel):
    staff_id: int
    restaurant_id: int


class AssignStaffRequest(BaseModel):
    staff_email: str
    manager_id: int
    restaurant_id: int
