from typing import List, Any

from pydantic import BaseModel


class IndividualImagesParameters(BaseModel):
    img_id: int
    img_path: Any


class RestaurantImagesParameters(BaseModel):
    images: List[IndividualImagesParameters]
