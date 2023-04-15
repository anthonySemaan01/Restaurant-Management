from fastapi import APIRouter, UploadFile, File, Depends
from persistence.sql_app.db_dependency import get_db
from sqlalchemy.orm import Session
from containers import Services
from domain.models.user_sign_up_request import UserSignUpRequest, UserUploadImage
from persistence.repositories.api_response import ApiResponse
from domain.contracts.services.abstract_user_management import AbstractUserManagement
from dependency_injector.wiring import inject, Provide
from domain.models.user_sign_in_request import UserSignInRequest

router = APIRouter()


@router.get("/customer_by_id")
@inject
async def get_customer_by_id(customer_id: int, db: Session = Depends(get_db),
                             user_management: AbstractUserManagement = Depends(
                                 Provide[Services.user_management])):
    return user_management.get_user_by_id(customer_id=customer_id, db=db)


@router.get("/all_customers")
@inject
async def get_all_users(db: Session = Depends(get_db), user_management: AbstractUserManagement = Depends(
    Provide[Services.user_management])):
    return user_management.get_all_users(db)

# TODO put staff application endpoints