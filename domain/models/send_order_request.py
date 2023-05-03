from typing import List

from pydantic import BaseModel


class Dish(BaseModel):
    dish_id: int
    count: int


class SendOrderRequest(BaseModel):
    table_id: int
    restaurant_id: int
    dishes: List[Dish]
