import os
from typing import List
from domain.contracts.services.abstract_restaurant_management import AbstractRestaurantManagement
from sqlalchemy.orm import Session
import persistence.sql_app.models as models
from domain.models.add_restaurant_request import AddRestaurantRequest
from domain.contracts.repositories.abstract_path_service import AbstractPathService
from fastapi import UploadFile, File
from domain.exceptions.restaurant_exception import AddRestaurantException
from shared.helpers.image_handler import load_image, save_image
from domain.models.restaurant_images_parameters import IndividualImagesParameters, RestaurantImagesParameters
import json


class RestaurantManagement(AbstractRestaurantManagement):

    def __init__(self, path_service: AbstractPathService):
        self.path_service = path_service

    def get_all_restaurants(self, db: Session):
        restaurants = db.query(models.Restaurant).all()
        for restaurant in restaurants:
            images_of_restaurant = []
            for image in json.loads(restaurant.images):
                images_of_restaurant.append(load_image(image["img_path"]))
            restaurant.images = images_of_restaurant
        return restaurants
        # to_return.images = [load_image(x["img_path"]) for x in json.loads(to_return.images)]

    def get_restaurant_by_id(self, restaurant_id: int, db: Session):
        pass

    def add_restaurant(self, db: Session, add_restaurant_request: AddRestaurantRequest):
        try:
            new_restaurant = models.Restaurant(name=add_restaurant_request.name, address=add_restaurant_request.address,
                                               phone_number=add_restaurant_request.phone_number,
                                               cuisine=add_restaurant_request.cuisine,
                                               website=add_restaurant_request.website,
                                               social_media_pages=add_restaurant_request.social_media_pages,
                                               hours_of_operation=add_restaurant_request.hours_of_operation,
                                               images=json.dumps([]))

            # TODO add restaurant to table of manager using manager id
            db.add(new_restaurant)
            db.commit()
        except Exception as e:
            raise AddRestaurantException(additional_message=e.__str__())
        return new_restaurant.restaurant_id

    def add_images_restaurant(self, db: Session, restaurant_id: int,
                              images: List[UploadFile]):
        images_list: List[IndividualImagesParameters] = []
        for index, image in enumerate(images):
            if not os.path.exists(os.path.join(os.getcwd(), self.path_service.paths.restaurants_images_path,
                                               f"rest{restaurant_id}")):
                os.mkdir(os.path.join(os.getcwd(), self.path_service.paths.restaurants_images_path,
                                      f"rest{restaurant_id}"))

            image_destination = os.path.join(os.getcwd(), self.path_service.paths.restaurants_images_path,
                                             f"rest{restaurant_id}",
                                             f"img{index}.png")
            if os.path.exists(image_destination):
                os.remove(image_destination)
            save_image(image, image_destination)
            images_list.append(IndividualImagesParameters(img_id=index, img_path=image_destination))
        restaurant = db.query(models.Restaurant).filter_by(restaurant_id=restaurant_id).first()
        restaurant.images = json.dumps([image.dict() for image in images_list])
        db.commit()
        to_return = db.query(models.Restaurant).filter_by(restaurant_id=restaurant_id).first()
        to_return.images = [load_image(x["img_path"]) for x in json.loads(to_return.images)]
        return to_return
