from fastapi import APIRouter, UploadFile, File, Depends
from persistence.sql_app.db_dependency import get_db
from sqlalchemy.orm import Session
from containers import Services
from domain.models.user_sign_up_request import UserSignUpRequest, UserUploadImage
from persistence.repositories.api_response import ApiResponse
from domain.contracts.services.abstract_user_management import AbstractUserManagement
from dependency_injector.wiring import inject, Provide
from domain.contracts.services.abstract_staff_management import AbstractStaffManagement

router = APIRouter()


@router.get("/get_by_id")
@inject
async def get_staff_by_id(staff_id: int, db: Session = Depends(get_db),
                          staff_management: AbstractStaffManagement = Depends(
                              Provide[Services.staff_management])):
    return staff_management.get_staff_by_id(staff_id=staff_id, db=db)


@router.get("/get_all")
@inject
async def get_all_staffs(db: Session = Depends(get_db), staff_management: AbstractStaffManagement = Depends(
    Provide[Services.staff_management])):
    return staff_management.get_all_staff(db)

# TODO put staff application endpoints
