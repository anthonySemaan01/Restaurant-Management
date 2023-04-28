import datetime
from abc import ABC, abstractmethod
from typing import List

from fastapi import UploadFile
from sqlalchemy.orm import Session

from domain.models.add_dishes_request import AddDishesRequest
from domain.models.add_restaurant_request import AddRestaurantRequest


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

    @abstractmethod
    def get_dates(self, restaurant_id: int, db: Session):
        pass

    @abstractmethod
    def get_available_tables_at_time(self, db: Session, restaurant_id, date_time: datetime.datetime):
        pass

    @abstractmethod
    def get_review(self, db: Session, restaurant_id: int):
        pass

    @abstractmethod
    def get_restaurant_by_name(self, db: Session, restaurant_name: str):
        pass

    @abstractmethod
    def get_restaurant_by_staff_id(self, db: Session, staff_id: int):
        pass

    @abstractmethod
    def get_restaurant_by_manager_id(self, db: Session, manager_id: int):
        pass
