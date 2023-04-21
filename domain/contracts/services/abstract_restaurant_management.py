from abc import ABC, abstractmethod
from fastapi import File, UploadFile
from sqlalchemy.orm import Session
from domain.models.add_restaurant_request import AddRestaurantRequest, AddRestaurantImagesRequest
from domain.models.add_dishes_request import AddDishesRequest
from typing import List


class AbstractRestaurantManagement(ABC):
    @abstractmethod
    def get_all_restaurants(self, db: Session):
        pass

    @abstractmethod
    def get_restaurant_by_id(self, restaurant_id: int, db: Session):
        pass

    @abstractmethod
    def add_restaurant(self, db: Session, add_restaurant_request: AddRestaurantRequest):
        pass

    @abstractmethod
    def add_images_restaurant(self, db: Session, restaurant_id: int,
                              images: List[UploadFile]):
        pass

    @abstractmethod
    def add_dishes(self, db: Session, add_dishes_request: AddDishesRequest):
        pass

    @abstractmethod
    def upload_dish_image(self, db: Session, dish_id: int, image: UploadFile):
        pass
