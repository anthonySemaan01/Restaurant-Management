from pydantic import BaseModel


class AssignManagerRequest(BaseModel):
    staff_id: int
    restaurant_id: int


class AssignStaffRequest(BaseModel):
    staff_id: int
    manager_id: int
    restaurant_id: int
