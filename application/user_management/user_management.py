from domain.contracts.services.abstract_user_management import AbstractUserManagement
from sqlalchemy.orm import Session
import persistence.sql_app.models as models


class UserManagement(AbstractUserManagement):
    def get_all_users(self, db: Session):
        data = db.query(models.Restaurant).all()
        return data
