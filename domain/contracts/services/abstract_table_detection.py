from abc import ABC, abstractmethod
from fastapi import File
from sqlalchemy.orm import Session


class AbstractTableDetection(ABC):
    @abstractmethod
    def detect_tables_return_json(self, db: Session, restaurant_id: int = None, image: bytes = File(...)):
        pass

    @abstractmethod
    def detect_tables_return_image(self, image: bytes = File(...)):
        pass
