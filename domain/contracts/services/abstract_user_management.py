from abc import ABC, abstractmethod
from sqlalchemy.orm import Session
from domain.models.user_sign_up_request import UserSignUpRequest
from fastapi import UploadFile
from domain.models.user_sign_in_request import UserSignInRequest
from domain.models.review_restaurant_request import ReviewRestaurantRequest
from domain.models.reserve_table_request import ReserveTableRequest


class AbstractUserManagement(ABC):
    @abstractmethod
    def get_all_users(self, db: Session):
        pass

    @abstractmethod
    def get_user_by_id(self, db: Session, customer_id: int):
        pass

    @abstractmethod
    def user_sign_in(self, db: Session, user_sign_in_request: UserSignInRequest):
        pass

    @abstractmethod
    def user_sign_up(self, db: Session, user_sign_up_request: UserSignUpRequest):
        pass

    @abstractmethod
    def upload_profile_image(self, db: Session, user_id: int, image: UploadFile):
        pass

    @abstractmethod
    def review_restaurant(self, db: Session, review_restaurant_request: ReviewRestaurantRequest):
        pass

    @abstractmethod
    def reserve_table(self, db: Session, reserve_table_request: ReserveTableRequest):
        pass
