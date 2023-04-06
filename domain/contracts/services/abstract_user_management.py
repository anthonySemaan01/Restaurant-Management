from abc import ABC, abstractmethod
from sqlalchemy.orm import Session
from domain.models.user_sign_up_request import UserSignUpRequest


class AbstractUserManagement(ABC):
    @abstractmethod
    def get_all_users(self, db: Session):
        pass

    @abstractmethod
    def get_user_by_id(self, db: Session, user_id: int):
        pass

    @abstractmethod
    def get_user_by_name(self, db: Session, user_name: str):
        pass

    @abstractmethod
    def user_sign_in(self, db: Session):
        pass

    @abstractmethod
    def user_sign_up(self, db: Session, user_sign_up_request: UserSignUpRequest):
        pass
