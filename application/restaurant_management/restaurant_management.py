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
from domain.models.add_dishes_request import AddDishesRequest
import json


class RestaurantManagement(AbstractRestaurantManagement):

    def __init__(self, path_service: AbstractPathService):
        self.path_service = path_service

    def get_all_restaurants(self, db: Session):
        restaurants = db.query(models.Restaurant).all()
        restaurant_list = list(restaurants)
        avg_rating_list: list = []
        for restaurant in restaurants:
            avg_rating = 0
            images_of_restaurant = []
            reviews = restaurant.reviews
            for review in reviews:
                avg_rating += int(review.rating)
            if len(reviews) != 0:
                avg_rating = avg_rating / len(reviews)

            avg_rating_list.append(avg_rating)
            for image in json.loads(restaurant.images):
                images_of_restaurant.append(load_image(image["img_path"]))
            restaurant.images = images_of_restaurant

        restaurants = list(restaurants)
        for index, restaurant in enumerate(restaurants):
            print(type(restaurant))
            restaurant = restaurant.__dict__
            restaurant["avg_rating"] = avg_rating_list[index]
        return restaurants

    def get_restaurant_by_id(self, restaurant_id: int, db: Session):
        restaurant = db.query(models.Restaurant).filter_by(restaurant_id=restaurant_id).first()
        avg_rating = 0
        images_of_restaurant = []
        for image in json.loads(restaurant.images):
            images_of_restaurant.append(load_image(image["img_path"]))
        restaurant.images = images_of_restaurant
        tables = restaurant.tables
        for review in restaurant.reviews:
            customer_review = review.customer.first_name

            avg_rating += int(review.rating)
        if len(restaurant.reviews) != 0:
            avg_rating = avg_rating / len(restaurant.reviews)
        for dish in restaurant.dishes:
            if dish.picture is not None:
                dish.picture = load_image(dish.picture)
        staffs = restaurant.staffs
        managers = restaurant.managers
        response_dict = restaurant.__dict__
        response_dict["avg_rating"] = avg_rating
        return response_dict

    def add_restaurant(self, db: Session, add_restaurant_request: AddRestaurantRequest):
        try:
            new_restaurant = models.Restaurant(name=add_restaurant_request.name, address=add_restaurant_request.address,
                                               phone_number=add_restaurant_request.phone_number,
                                               cuisine=add_restaurant_request.cuisine,
                                               website=add_restaurant_request.website,
                                               social_media_pages=add_restaurant_request.social_media_pages,
                                               hours_of_operation=add_restaurant_request.hours_of_operation,
                                               images=json.dumps([]))
            db.add(new_restaurant)
            db.commit()
            staff = db.query(models.Staff).filter_by(staff_id=add_restaurant_request.staff_id).first()
            new_manager = models.Manager(restaurant_id=new_restaurant.restaurant_id, email=staff.email,
                                         password=staff.password, phone_nb=staff.phone_nb,
                                         first_name=staff.first_name, last_name=staff.last_name,
                                         date_of_birth=staff.date_of_birth, picture=staff.picture)
            # db.delete(staff)
            db.add(new_manager)
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

    def add_dishes(self, db: Session, add_dishes_request: AddDishesRequest):
        restaurant_id = add_dishes_request.restaurant_id
        new_dish = models.Dish(restaurant_id=restaurant_id, name=add_dishes_request.name,
                               price=add_dishes_request.price,
                               description=add_dishes_request.description)
        db.add(new_dish)
        db.commit()
        return db.query(models.Restaurant).filter_by(restaurant_id=restaurant_id).first().dishes

    def upload_dish_image(self, db: Session, dish_id: int, image: UploadFile):
        image_destination = os.path.join(os.getcwd(), self.path_service.paths.dishes_images_path, f"img{dish_id}.png")

        if os.path.exists(image_destination):
            os.remove(image_destination)
        save_image(image, image_destination)
        dish = db.query(models.Dish).filter_by(dish_id=dish_id).first()
        dish.picture = image_destination
        db.commit()

        to_return = db.query(models.Dish).filter_by(dish_id=dish_id).first()
        to_return.picture = load_image(to_return.picture)
        return to_return
