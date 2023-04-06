from abc import ABC, abstractmethod
from sqlalchemy.orm import Session


class AbstractUserManagement(ABC):
    @abstractmethod
    def get_all_users(self, db: Session):
        pass
