import os
from fastapi import UploadFile
from sqlalchemy.orm import Session
import persistence.sql_app.models as models
from domain.contracts.services.abstract_staff_management import AbstractStaffManagement
from domain.contracts.repositories.abstract_path_service import AbstractPathService
from domain.models.staff_sign_up_request import StaffSignUpRequest
from domain.exceptions.staff_exception import StaffSignInException, StaffSignUpException
from shared.helpers.image_handler import load_image, save_image
from domain.models.staff_sign_in_request import StaffSignInRequest


class StaffManagement(AbstractStaffManagement):
    def __init__(self, path_service: AbstractPathService):
        self.path_service = path_service

    def get_all_staff(self, db: Session):
        data = db.query(models.Staff).all()
        return data

    def get_staff_by_id(self, db: Session, staff_id: int):
        staff = db.query(models.Staff).filter_by(staff_id=staff_id).first()
        if staff.picture:
            staff.picture = load_image(staff.picture)
        return staff

    def staff_sign_in(self, db: Session, staff_sign_in_request: StaffSignInRequest):
        staff = db.query(models.Staff).filter_by(email=staff_sign_in_request.email).first()

        if staff is not None:
            if staff_sign_in_request.password == staff.password:
                return True, staff.customer_id

        return False, -1

    def staff_sign_up(self, db: Session, staff_sign_up_request: StaffSignUpRequest):
        try:
            new_staff = models.Staff(email=staff_sign_up_request.email, password=staff_sign_up_request.password,
                                     phone_nb=staff_sign_up_request.password,
                                     first_name=staff_sign_up_request.first_name,
                                     last_name=staff_sign_up_request.last_name,
                                     date_of_birth=staff_sign_up_request.date_of_birth)
            db.add(new_staff)
            db.commit()
        except Exception as e:
            raise StaffSignUpException(additional_message=e.__str__())
        return new_staff.staff_id

    def upload_profile_image(self, db: Session, staff_id: int, image: UploadFile):
        image_destination = os.path.join(os.getcwd(), self.path_service.paths.staffs_images_path, f"img{staff_id}.png")

        if os.path.exists(image_destination):
            os.remove(image_destination)
        save_image(image, image_destination)
        staff = db.query(models.Staff).filter_by(staff_id=staff_id).first()
        staff.picture = image_destination
        db.commit()

        to_return = db.query(models.Staff).filter_by(staff_id=staff_id).first()
        to_return.picture = load_image(to_return.picture)
        return to_return
