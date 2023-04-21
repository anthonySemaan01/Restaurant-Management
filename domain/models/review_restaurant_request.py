from pydantic import BaseModel


class ReviewRestaurantRequest(BaseModel):
    restaurant_id: int
    customer_id: int
    rating: int
    comment: str
