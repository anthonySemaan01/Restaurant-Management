from abc import ABC, abstractmethod
from sqlalchemy.orm import Session
from domain.models.user_sign_up_request import UserSignUpRequest
from fastapi import File


class AbstractTableDetection(ABC):
    @abstractmethod
    def detect_tables_return_json(self, image: bytes = File(...)):
        pass

    @abstractmethod
    def detect_tables_return_image(self, image: bytes = File(...)):
        pass
