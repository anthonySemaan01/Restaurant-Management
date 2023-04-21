from abc import ABC, abstractmethod
from sqlalchemy.orm import Session
from domain.models.staff_sign_up_request import StaffSignUpRequest
from fastapi import UploadFile, File
from domain.models.staff_sign_in_request import StaffSignInRequest


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
