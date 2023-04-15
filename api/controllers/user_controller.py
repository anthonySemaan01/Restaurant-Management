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


@router.post("/user_sign_up")
@inject
async def user_sign_up(user_sign_up_request: UserSignUpRequest, db: Session = Depends(get_db),
                       user_management: AbstractUserManagement = Depends(
                           Provide[Services.user_management])):
    try:
        id_of_new_user = user_management.user_sign_up(db, user_sign_up_request)
        return ApiResponse(success=True, data=id_of_new_user)
    except Exception as e:
        return ApiResponse(success=False, error=e.__str__())


@router.post("/user_sign_in")
@inject
async def user_sign_in(user_sign_in_request: UserSignInRequest, db: Session = Depends(get_db),
                       user_management: AbstractUserManagement = Depends(
                           Provide[Services.user_management])):
    try:
        success, customer_id = user_management.user_sign_in(db, user_sign_in_request)
        print(success, customer_id)
        if success:
            return ApiResponse(success=True, data=customer_id)
        else:
            return ApiResponse(success=False, error="Incorrect Username or Password")
    except Exception as e:
        return ApiResponse(success=False, error=e.__str__())


@router.post("/user_upload_profile_picture")
@inject
async def user_upload_profile_image(image: UploadFile, user_id: UserUploadImage = Depends(),
                                    db: Session = Depends(get_db),
                                    user_management: AbstractUserManagement = Depends(
                                        Provide[Services.user_management])):
    try:
        user = user_management.upload_profile_image(db=db, user_id=user_id.id, image=image)
        return ApiResponse(success=True, data=user)
    except Exception as e:
        return ApiResponse(success=False, error=e.__str__())
