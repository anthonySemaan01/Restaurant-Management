from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from containers import Services
from domain.contracts.services.abstract_manager_management import AbstractManagerManagement
from domain.models.manager_requests import AssignManagerRequest, AssignStaffRequest
from persistence.sql_app.db_dependency import get_db

router = APIRouter()


@router.get("/get_by_id")
@inject
async def get_manager_by_id(manager_id: int, db: Session = Depends(get_db),
                            manager_management: AbstractManagerManagement = Depends(
                                Provide[Services.manager_management])):
    return manager_management.get_manager_by_id(manager_id=manager_id, db=db)


@router.get("/all_managers")
@inject
async def get_all_managers(db: Session = Depends(get_db),
                           manager_management: AbstractManagerManagement = Depends(
                               Provide[Services.manager_management])):
    return manager_management.get_all_managers(db=db)


@router.post("/assign_manager_to_restaurant")
@inject
async def assign_manager_to_restaurant(assign_manager_request: AssignManagerRequest, db: Session = Depends(get_db),
                                       manager_management: AbstractManagerManagement = Depends(
                                           Provide[Services.manager_management])):
    return manager_management.assign_manager_to_restaurant(assign_manager_request=assign_manager_request, db=db)


@router.post("/assign_staff_to_restaurant")
@inject
async def assign_staff_to_restaurant(assign_staff_request: AssignStaffRequest, db: Session = Depends(get_db),
                                     manager_management: AbstractManagerManagement = Depends(
                                         Provide[Services.manager_management])):
    return manager_management.assign_staff_to_restaurant(assign_staff_request=assign_staff_request, db=db)
