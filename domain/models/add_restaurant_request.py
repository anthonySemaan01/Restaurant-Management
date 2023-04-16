from pydantic import BaseModel
from typing import Dict, List


class AddRestaurantRequest(BaseModel):
    name: str
    address: str
    phone_number: str
    cuisine: List[str]
    website: str
    social_media_pages: dict
    hours_of_operation: str
    manager_id: int


class AddRestaurantImagesRequest(BaseModel):
    restaurant_id: int
