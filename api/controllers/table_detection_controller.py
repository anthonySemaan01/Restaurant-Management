from fastapi import APIRouter, UploadFile, File, Depends
from containers import Services
from persistence.sql_app.db_dependency import get_db
from sqlalchemy.orm import Session
from persistence.repositories.api_response import ApiResponse
from domain.contracts.services.abstract_table_detection import AbstractTableDetection
from dependency_injector.wiring import inject, Provide
from domain.models.add_restaurant_request import AddRestaurantImagesRequest
from typing import Optional

router = APIRouter()


@router.post("/image-to-json")
@inject
async def detect_tables_return_json(add_restaurant_request: AddRestaurantImagesRequest = Depends(),
                                    db: Session = Depends(get_db), image: bytes = File(...),
                                    table_detection: AbstractTableDetection = Depends(
                                        Provide[Services.table_detection])):
    return ApiResponse(success=True,
                       data=table_detection.detect_tables_return_json(db=db,
                                                                      restaurant_id=add_restaurant_request.restaurant_id,
                                                                      image=image))


@router.post("/image-to-image")
@inject
async def detect_tables_return_image(image: bytes = File(...), table_detection: AbstractTableDetection = Depends(
    Provide[Services.table_detection])):
    return table_detection.detect_tables_return_image(image)
