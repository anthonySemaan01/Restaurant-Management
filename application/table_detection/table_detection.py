import io
import json

from PIL import Image
from fastapi import File, UploadFile
from sqlalchemy.orm import Session
from starlette.responses import Response

import persistence.sql_app.models as models
from core.images.image_processor import get_image_from_bytes
from core.model.model_configuation import get_yolov5
from domain.contracts.services.abstract_table_detection import AbstractTableDetection
from persistence.services.path_service import AbstractPathService

model = get_yolov5()


class TableDetection(AbstractTableDetection):
    def __init__(self, path_service: AbstractPathService):
        self.path_service = path_service

    def detect_tables_return_json(self, image: UploadFile, db: Session, restaurant_id: int = None):
        input_image, input_image_width, input_image_height = get_image_from_bytes(image)
        results = model(input_image)
        detect_res = results.pandas().xyxy[0].to_json(orient="records")
        detect_res = json.loads(detect_res)
        restaurant = db.query(models.Restaurant).filter_by(restaurant_id=restaurant_id).first()
        restaurant.dimensions = {"width": input_image_width, "height": input_image_height}
        db.commit()

        for table in detect_res:
            print(table)
            print(type(table))
            new_table = models.Table(restaurant_id=restaurant_id, capacity=4, location=table)
            db.add(new_table)
        db.commit()
        return detect_res

    def detect_tables_return_image(self, image: UploadFile):
        input_image, input_image_width, input_image_height = get_image_from_bytes(image)
        results = model(input_image)
        results.render()
        for img in results.ims:
            bytes_io = io.BytesIO()
            img_base64 = Image.fromarray(img)
            img_base64.save(bytes_io, format="jpeg")
        return Response(content=bytes_io.getvalue(),
                        media_type="image/jpeg")
