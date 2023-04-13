from domain.contracts.services.abstract_user_management import AbstractUserManagement
from sqlalchemy.orm import Session
import persistence.sql_app.models as models
from domain.models.user_sign_up_request import UserSignUpRequest
from domain.exceptions.user_exception import UserSignInException, UserSignUpException
from fastapi import UploadFile, File


class UserManagement(AbstractUserManagement):
    def get_user_by_id(self, db: Session):
        pass

    def get_user_by_name(self, db: Session):
        pass

    def user_sign_in(self, db: Session):
        pass

    def user_sign_up(self, db: Session, user_sign_up_request: UserSignUpRequest, image: UploadFile = File(...)):

        try:
            new_customer = models.Customer(email=user_sign_up_request.email, password=user_sign_up_request.password,
                                           phone_nb=user_sign_up_request.password,
                                           first_name=user_sign_up_request.first_name,
                                           last_name=user_sign_up_request.last_name,
                                           picture=user_sign_up_request.picture,
                                           date_of_birth=user_sign_up_request.date_of_birth)
            db.add(new_customer)
            db.commit()
        except Exception as e:
            raise UserSignUpException(additional_message=e.__str__())
        return new_customer.customer_id

    def get_all_users(self, db: Session):
        data = db.query(models.Customer).all()
        return data
