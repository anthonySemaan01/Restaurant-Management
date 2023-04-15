import os
from pydantic import BaseModel


class ApiPaths(BaseModel):
    restaurants_images_path: str
    users_images_path: str
    staffs_images_path: str
