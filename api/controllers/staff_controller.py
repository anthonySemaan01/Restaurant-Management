from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, UploadFile, Depends
from sqlalchemy.orm import Session

from containers import Services
from domain.contracts.services.abstract_staff_management import AbstractStaffManagement
from domain.models.send_order_request import SendOrderRequest
from domain.models.staff_sign_up_request import StaffSignUpRequest, StaffUploadImage
from persistence.repositories.api_response import ApiResponse
from persistence.sql_app.db_dependency import get_db

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


@router.post("/sign_up")
@inject
async def staff_sign_up(staff_sign_up_request: StaffSignUpRequest, db: Session = Depends(get_db),
                        staff_management: AbstractStaffManagement = Depends(
                            Provide[Services.staff_management])):
    try:
        data, status = staff_management.staff_sign_up(db, staff_sign_up_request)
        return ApiResponse(success=status, data=data)
    except Exception as e:
        return ApiResponse(success=False, error=e.__str__())


# @router.post("/sign_in")
# @inject
# async def user_sign_in(staff_sign_in_request: StaffSignInRequest, db: Session = Depends(get_db),
#                        staff_management: AbstractStaffManagement = Depends(
#                            Provide[Services.staff_management])):
#     try:
#         success, staff_id = staff_management.staff_sign_in(db, staff_sign_in_request)
#         if success:
#             return ApiResponse(success=True, data=staff_id)
#         else:
#             return ApiResponse(success=False, error="Incorrect Username or Password")
#     except Exception as e:
#         return ApiResponse(success=False, error=e.__str__())


@router.post("/upload_profile_picture")
@inject
async def staff_upload_profile_image(image: UploadFile, staff_id: StaffUploadImage = Depends(),
                                     db: Session = Depends(get_db),
                                     staff_management: AbstractStaffManagement = Depends(
                                         Provide[Services.staff_management])):
    try:
        user = staff_management.upload_profile_image(db=db, staff_id=staff_id.id, image=image)
        return ApiResponse(success=True, data=user)
    except Exception as e:
        return ApiResponse(success=False, error=e.__str__())


@router.get("/get_bookings")
@inject
async def get_all_bookings(restaurant_id: int, db: Session = Depends(get_db),
                           staff_management: AbstractStaffManagement = Depends(
                               Provide[Services.staff_management])):
    return staff_management.get_bookings(restaurant_id=restaurant_id, db=db)


@router.post("/send_order")
@inject
async def send_order(send_order_request: SendOrderRequest, db: Session = Depends(get_db),
                     staff_management: AbstractStaffManagement = Depends(
                         Provide[Services.staff_management])):
    try:
        order, status = staff_management.send_order(db=db, send_order_request=send_order_request)
        return ApiResponse(success=status, data=order)
    except Exception as e:
        return ApiResponse(success=False, error=e.__str__())
