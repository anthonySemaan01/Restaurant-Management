from sqlalchemy.orm import Session

import persistence.sql_app.models as models
from domain.exceptions.db_exception import DBException


# def get_point_cloud_by_path(db: Session, path: str):
#     return db.query(point_cloud_model.PointCloud).filter(point_cloud_model.PointCloud.path == path).first()
def get_restaurant_by_name(db: Session, name: str):
    return db.query(models.Restaurant).filter(models.Restaurant.name == name).first()


def get_all_restaurants(db: Session, skip: int = 0,
                        limit: int = 100) -> list:  # Always set return type and use from typing import List, Dict, Optional so you can specify for example List[int] or List[PointCloud]
    try:
        return db.query(models.Restaurant).offset(skip).limit(limit).all()
    except Exception as e:
        raise DBException(additional_message=e.__str__())

# def create_point_cloud(db: Session, point_count: int, path: str) -> \
#         ocr_api.persistence.sqlite_db.point_cloud_model.PointCloud:  # Just import it and only use PointCloud
#     point_cloud = point_cloud_model.PointCloud(points_count=point_count, path=path)
#     try:
#         db.add(point_cloud)
#         db.commit()
#         db.refresh(point_cloud)
#         return point_cloud
#     except Exception as e:
#         raise DBException(additional_message=e.__str__())
