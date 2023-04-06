from fastapi import APIRouter, Response, HTTPException, UploadFile, File, Depends
from persistence.sql_app.db_dependency import get_db
from sqlalchemy.orm import Session
from containers import Services
from domain.models.user_sign_up_request import UserSignUpRequest

router = APIRouter()
user_management = Services.user_management()


@router.get("/all_customers")
async def get_all_users(db: Session = Depends(get_db)):
    return user_management.get_all_users(db)


@router.post("/user_sign_up")
async def user_sign_up(user_sign_up_request: UserSignUpRequest, db: Session = Depends(get_db)):
    return user_management.user_sign_up(db, user_sign_up_request)
