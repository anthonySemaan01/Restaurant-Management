from abc import ABC, abstractmethod

from fastapi import File, UploadFile
from sqlalchemy.orm import Session


class AbstractTableDetection(ABC):
    @abstractmethod
    def detect_tables_return_json(self, image: UploadFile, db: Session, restaurant_id: int = None):
        pass

    @abstractmethod
    def detect_tables_return_image(self, image: UploadFile):
        pass
