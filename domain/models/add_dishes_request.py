from pydantic import BaseModel


class AddDishesRequest(BaseModel):
    restaurant_id: int
    name: str
    price: float
    description: str


class DishUploadImage(BaseModel):
    dish_id: int
