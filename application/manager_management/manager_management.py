from sqlalchemy import func
from sqlalchemy.orm import Session

import persistence.sql_app.models as models
from domain.contracts.services.abstract_manager_management import AbstractManagerManagement
from domain.models.manager_requests import AssignManagerRequest, AssignStaffRequest
from persistence.services.path_service import AbstractPathService
from shared.helpers.image_handler import load_image


class ManagerManagement(AbstractManagerManagement):
    def __init__(self, path_service: AbstractPathService):
        self.path_service = path_service

    def get_manager_by_id(self, manager_id: int, db: Session):
        manager = db.query(models.Manager).filter_by(manager_id=manager_id).first()
        if manager.picture:
            manager.picture = load_image(manager.picture)
        return manager

    def get_all_managers(self, db: Session):
        managers = db.query(models.Manager).all()
        return managers

    def assign_manager_to_restaurant(self, assign_manager_request: AssignManagerRequest, db: Session):
        staff = db.query(models.Staff).filter_by(staff_id=assign_manager_request.staff_id).first()
        manager = models.Manager(email=staff.email, first_name=staff.first_name, last_name=staff.last_name,
                                 password=staff.password, phone_nb=staff.phone_nb, date_of_birth=staff.date_of_birth,
                                 picture=staff.picture)
        manager.restaurant_id = assign_manager_request.restaurant_id

        db.add(manager)
        db.delete(staff)
        db.commit()
        print(manager.manager_id)
        print(manager.restaurant)
        return manager

    def assign_staff_to_restaurant(self, assign_staff_request: AssignStaffRequest, db: Session):
        staff = db.query(models.Staff).filter(
            func.lower(models.Staff.email) == assign_staff_request.staff_email.lower()).first()
        if staff is None:
            return False, "No such staff account found!"
        if staff.restaurant_id is None:
            staff.restaurant_id = assign_staff_request.restaurant_id
            staff.manager_id = assign_staff_request.manager_id
            db.commit()
            return True, f"Staff {assign_staff_request.staff_email} added"
        else:
            return False, "Staff already working in another restaurant"
