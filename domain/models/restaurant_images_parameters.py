from pydantic import BaseModel
from typing import Dict, List, Any


class IndividualImagesParameters(BaseModel):
    img_id: int
    img_path: Any


class RestaurantImagesParameters(BaseModel):
    images: List[IndividualImagesParameters]
