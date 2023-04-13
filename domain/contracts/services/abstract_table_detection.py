from abc import ABC, abstractmethod
from fastapi import File


class AbstractTableDetection(ABC):
    @abstractmethod
    def detect_tables_return_json(self, image: bytes = File(...)):
        pass

    @abstractmethod
    def detect_tables_return_image(self, image: bytes = File(...)):
        pass
