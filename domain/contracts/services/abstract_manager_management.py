from abc import ABC, abstractmethod

from sqlalchemy.orm import Session

from domain.models.manager_requests import AssignManagerRequest, AssignStaffRequest


class AbstractManagerManagement(ABC):

    @abstractmethod
    def get_all_managers(self, db: Session):
        pass

    @abstractmethod
    def get_manager_by_id(self, manager_id: int, db: Session):
        pass

    @abstractmethod
    def assign_manager_to_restaurant(self, assign_manager_request: AssignManagerRequest, db: Session):
        pass

    @abstractmethod
    def assign_staff_to_restaurant(self, assign_staff_request: AssignStaffRequest, db: Session):
        pass
