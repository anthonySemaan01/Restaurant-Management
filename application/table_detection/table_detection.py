from domain.contracts.services.abstract_table_detection import AbstractTableDetection
from sqlalchemy.orm import Session
import persistence.sql_app.models as models
from domain.models.user_sign_up_request import UserSignUpRequest
from domain.exceptions.user_exception import UserSignInException, UserSignUpException
from core.model.model_configuation import get_yolov5
from core.images.image_processor import get_image_from_bytes
from starlette.responses import Response
import json
from fastapi import File
from PIL import Image
import io
from persistence.services.path_service import AbstractPathService

model = get_yolov5()


class TableDetection(AbstractTableDetection):
    def __init__(self, path_service: AbstractPathService):
        self.path_service = path_service

    def detect_tables_return_json(self, image: bytes = File(...)):
        input_image = get_image_from_bytes(image)
        results = model(input_image)
        detect_res = results.pandas().xyxy[0].to_json(orient="records")
        detect_res = json.loads(detect_res)
        return detect_res

    def detect_tables_return_image(self, image: bytes = File(...)):
        input_image = get_image_from_bytes(image)
        results = model(input_image)
        results.render()
        for img in results.ims:
            bytes_io = io.BytesIO()
            img_base64 = Image.fromarray(img)
            img_base64.save(bytes_io, format="jpeg")
        return Response(content=bytes_io.getvalue(),
                        media_type="image/jpeg")
