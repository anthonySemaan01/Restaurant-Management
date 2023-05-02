from typing import List

from pydantic import BaseModel


class Dish(BaseModel):
    dish_id: int
    num: int


class SendOrderRequest(BaseModel):
    table_id: int
    dishes: List[Dish]
