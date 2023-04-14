import os

from domain.contracts.services.abstract_user_management import AbstractUserManagement
from sqlalchemy.orm import Session
import persistence.sql_app.models as models
from domain.models.user_sign_up_request import UserSignUpRequest
from domain.exceptions.user_exception import UserSignUpException
from domain.contracts.repositories.abstract_path_service import AbstractPathService
from fastapi import UploadFile, File
from sqlalchemy import create_engine, Column, Integer, String
from shared.helpers.image_handler import load_image, save_image


class UserManagement(AbstractUserManagement):
    def __init__(self, path_service: AbstractPathService):
        self.path_service = path_service

    def get_user_by_id(self, db: Session):
        pass

    def get_user_by_name(self, db: Session):
        pass

    def user_sign_in(self, db: Session):
        pass

    def user_sign_up(self, db: Session, user_sign_up_request: UserSignUpRequest):
        try:
            new_customer = models.Customer(email=user_sign_up_request.email, password=user_sign_up_request.password,
                                           phone_nb=user_sign_up_request.password,
                                           first_name=user_sign_up_request.first_name,
                                           last_name=user_sign_up_request.last_name,
                                           date_of_birth=user_sign_up_request.date_of_birth)
            db.add(new_customer)
            db.commit()
        except Exception as e:
            raise UserSignUpException(additional_message=e.__str__())
        return new_customer.customer_id

    def upload_profile_image(self, db: Session, user_id: Integer, image: UploadFile):
        image_destination = os.path.join(os.getcwd(), self.path_service.paths.users_images_path, f"img{user_id}.png")
        print(image_destination)
        print(os.path.exists(image_destination))
        if os.path.exists(image_destination):
            os.remove(image_destination)
        save_image(image, image_destination)
        user = db.query(models.Customer).filter_by(customer_id=user_id).first()
        user.picture = image_destination
        db.commit()

        to_return = db.query(models.Customer).filter_by(customer_id=user_id).first()
        to_return.picture = load_image(to_return.picture)
        return to_return

    def get_all_users(self, db: Session):
        data = db.query(models.Customer).all()
        return data
