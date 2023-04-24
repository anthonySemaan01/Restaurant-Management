from sqlalchemy.orm import Session
from domain.models.manager_requests import AssignManagerRequest, AssignStaffRequest
from domain.contracts.services.abstract_manager_management import AbstractManagerManagement
from persistence.services.path_service import AbstractPathService


class ManagerManagement(AbstractManagerManagement):
    def __init__(self, path_service: AbstractPathService):
        self.path_service = path_service

    def get_manager_by_id(self, manager_id: int, db: Session):
        pass

    def get_all_managers(self, db: Session):
        pass

    def assign_manager_to_restaurant(self, assign_manager_request: AssignManagerRequest, db: Session):
        pass

    def assign_staff_to_restaurant(self, assign_staff_request: AssignStaffRequest, db: Session):
        pass
