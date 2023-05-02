from abc import ABC, abstractmethod

from fastapi import UploadFile
from sqlalchemy.orm import Session

from domain.models.send_order_request import SendOrderRequest
from domain.models.staff_sign_in_request import StaffSignInRequest
from domain.models.staff_sign_up_request import StaffSignUpRequest


class AbstractStaffManagement(ABC):
    @abstractmethod
    def get_all_staff(self, db: Session):
        pass

    @abstractmethod
    def get_staff_by_id(self, db: Session, staff_id: int):
        pass

    @abstractmethod
    def staff_sign_in(self, db: Session, staff_sign_in_request: StaffSignInRequest):
        pass

    @abstractmethod
    def staff_sign_up(self, db: Session, staff_sign_up_request: StaffSignUpRequest):
        pass

    @abstractmethod
    def upload_profile_image(self, db: Session, staff_id: int, image: UploadFile):
        pass

    @abstractmethod
    def get_bookings(self, db: Session, restaurant_id: int):
        pass

    def send_order(self, db: Session, send_order_request: SendOrderRequest):
        pass
