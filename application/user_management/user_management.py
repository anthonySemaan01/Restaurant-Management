from domain.contracts.services.abstract_user_management import AbstractUserManagement
from sqlalchemy.orm import Session
import persistence.sql_app.models as models
from domain.models.user_sign_up_request import UserSignUpRequest


class UserManagement(AbstractUserManagement):
    def get_user_by_id(self, db: Session):
        pass

    def get_user_by_name(self, db: Session):
        pass

    def user_sign_in(self, db: Session):
        pass

    def user_sign_up(self, db: Session, user_sign_up_request: UserSignUpRequest):
        print(user_sign_up_request.json())
        new_customer = models.Customer(email=user_sign_up_request.email, password=user_sign_up_request.password,
                                       phone_nb=user_sign_up_request.password, first_name=user_sign_up_request.first_name,
                                       last_name=user_sign_up_request.last_name, picture=user_sign_up_request.picture,
                                       date_of_birth=user_sign_up_request.date_of_birth)
        db.add(new_customer)
        db.commit()
        return new_customer.customer_id

    def get_all_users(self, db: Session):
        data = db.query(models.Customer).all()
        return data
