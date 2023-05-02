from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, UploadFile, Depends
from sqlalchemy.orm import Session

from containers import Services
from domain.contracts.services.abstract_user_management import AbstractUserManagement
from domain.models.reserve_table_request import ReserveTableRequest
from domain.models.review_restaurant_request import ReviewRestaurantRequest
from domain.models.user_sign_in_request import UserSignInRequest
from domain.models.user_sign_up_request import UserSignUpRequest, UserUploadImage
from persistence.repositories.api_response import ApiResponse
from persistence.sql_app.db_dependency import get_db

router = APIRouter()


@router.get("/get_by_id")
@inject
async def get_customer_by_id(customer_id: int, db: Session = Depends(get_db),
                             user_management: AbstractUserManagement = Depends(
                                 Provide[Services.user_management])):
    return user_management.get_user_by_id(customer_id=customer_id, db=db)


@router.get("/get_all")
@inject
async def get_all_users(db: Session = Depends(get_db), user_management: AbstractUserManagement = Depends(
    Provide[Services.user_management])):
    return user_management.get_all_users(db)


@router.post("/sign_up")
@inject
async def user_sign_up(user_sign_up_request: UserSignUpRequest, db: Session = Depends(get_db),
                       user_management: AbstractUserManagement = Depends(
                           Provide[Services.user_management])):
    try:
        id_of_new_user = user_management.user_sign_up(db, user_sign_up_request)
        return ApiResponse(success=True, data=id_of_new_user)
    except Exception as e:
        return ApiResponse(success=False, error=e.__str__())


@router.post("/sign_in")
@inject
async def user_sign_in(user_sign_in_request: UserSignInRequest, db: Session = Depends(get_db),
                       user_management: AbstractUserManagement = Depends(
                           Provide[Services.user_management])):
    try:
        success, category, found_id, restaurant_id = user_management.user_sign_in(db, user_sign_in_request)
        if success:
            return ApiResponse(success=True, data={
                "category": category,
                "id": found_id,
                "restaurant_id": restaurant_id
            })
        else:
            return ApiResponse(success=False, error="Incorrect Username or Password")
    except Exception as e:
        return ApiResponse(success=False, error=e.__str__())


@router.post("/upload_profile_picture")
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


@router.post("/review_restaurant")
@inject
async def review_restaurant(review_restaurant_request: ReviewRestaurantRequest, db: Session = Depends(get_db),
                            user_management: AbstractUserManagement = Depends(
                                Provide[Services.user_management])):
    return user_management.review_restaurant(db=db, review_restaurant_request=review_restaurant_request)


@router.post("/reserve_table")
@inject
async def reserve_table(reserve_table_request: ReserveTableRequest, db: Session = Depends(get_db),
                        user_management: AbstractUserManagement = Depends(
                            Provide[Services.user_management])):
    return user_management.reserve_table(db=db, reserve_table_request=reserve_table_request)


@router.get("/all_booking")
@inject
async def get_all_bookings(customer_id: int, db: Session = Depends(get_db),
                           user_management: AbstractUserManagement = Depends(
                               Provide[Services.user_management])):
    return user_management.get_all_bookings(db=db, user_id=customer_id)
