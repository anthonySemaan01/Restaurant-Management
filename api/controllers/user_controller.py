from fastapi import APIRouter, Response, HTTPException, UploadFile, File, Depends
from persistence.sql_app.db_dependency import get_db
from sqlalchemy.orm import Session
from containers import Services

router = APIRouter()
user_management = Services.user_management()


@router.get("/all_users")
async def get_all_users(db: Session = Depends(get_db)):
    return user_management.get_all_users(db)
