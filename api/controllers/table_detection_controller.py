from fastapi import APIRouter, UploadFile, File
from containers import Services
from persistence.repositories.api_response import ApiResponse

router = APIRouter()
table_detection = Services.table_detection()


@router.post("/image-to-json")
async def detect_tables_return_json(image: bytes = File(...)):
    return ApiResponse(success=True,
                       data=table_detection.detect_tables_return_json(image))


@router.post("/image-to-image")
async def detect_tables_return_image(image: bytes = File(...)):
    return table_detection.detect_tables_return_image(image)
