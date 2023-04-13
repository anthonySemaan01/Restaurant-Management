from fastapi import APIRouter, UploadFile, File, Depends
from persistence.sql_app.db_dependency import get_db
from sqlalchemy.orm import Session
from containers import Services
from domain.models.user_sign_up_request import UserSignUpRequest
from persistence.repositories.api_response import ApiResponse

router = APIRouter()
user_management = Services.user_management()


@router.get("/all_customers")
async def get_all_users(db: Session = Depends(get_db)):
    return user_management.get_all_users(db)


@router.post("/user_sign_up")
async def user_sign_up(user_sign_up_request: UserSignUpRequest, image: UploadFile = File(...),
                       db: Session = Depends(get_db)):
    # TODO: add path service and store images in directory, take path, and store it in db
    try:
        id_of_new_user = user_management.user_sign_up(db, user_sign_up_request, image)
        return ApiResponse(success=True, data=id_of_new_user)
    except Exception as e:
        return ApiResponse(success=False, error=e.__str__())
