from fastapi import APIRouter, UploadFile, File, Depends
from containers import Services
from persistence.repositories.api_response import ApiResponse
from domain.contracts.services.abstract_table_detection import AbstractTableDetection
from dependency_injector.wiring import inject, Provide

router = APIRouter()


@router.post("/image-to-json")
@inject
async def detect_tables_return_json(image: bytes = File(...), table_detection: AbstractTableDetection = Depends(
    Provide[Services.table_detection])):
    return ApiResponse(success=True,
                       data=table_detection.detect_tables_return_json(image))


@router.post("/image-to-image")
@inject
async def detect_tables_return_image(image: bytes = File(...), table_detection: AbstractTableDetection = Depends(
    Provide[Services.table_detection])):
    return table_detection.detect_tables_return_image(image)
