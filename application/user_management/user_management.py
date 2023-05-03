import datetime
import os

from fastapi import UploadFile
from sqlalchemy import Integer
from sqlalchemy import func
from sqlalchemy.orm import Session

import persistence.sql_app.models as models
from core.nlp.nlp import start_inference
from domain.contracts.repositories.abstract_path_service import AbstractPathService
from domain.contracts.services.abstract_user_management import AbstractUserManagement
from domain.exceptions.user_exception import UserSignUpException
from domain.models.reserve_table_request import ReserveTableRequest
from domain.models.review_restaurant_request import ReviewRestaurantRequest
from domain.models.user_sign_in_request import UserSignInRequest
from domain.models.user_sign_up_request import UserSignUpRequest
from shared.helpers.image_handler import load_image, save_image
from shared.helpers.restaurant_review_calculation import get_restaurant_review_rate


class UserManagement(AbstractUserManagement):

    def __init__(self, path_service: AbstractPathService):
        self.path_service = path_service

    def get_user_by_id(self, db: Session, customer_id: int):
        customer = db.query(models.Customer).filter_by(customer_id=customer_id).first()
        if customer.picture:
            customer.picture = load_image(customer.picture)
        return customer

    def user_sign_in(self, db: Session, user_sign_in_request: UserSignInRequest):

        customer = db.query(models.Customer).filter(
            func.lower(models.Customer.email) == user_sign_in_request.email.lower()).first()
        staff = db.query(models.Staff).filter(
            func.lower(models.Staff.email) == user_sign_in_request.email.lower()).first()
        manager = db.query(models.Manager).filter(
            func.lower(models.Manager.email) == user_sign_in_request.email.lower()).first()

        if customer is not None:
            if user_sign_in_request.password == customer.password:
                return True, "customer", customer.customer_id, -1

        elif staff is not None:
            if user_sign_in_request.password == staff.password:
                restaurant = staff.restaurant_id
                if restaurant is None:
                    restaurant = -1
                return True, "staff", staff.staff_id, restaurant

        elif manager is not None:
            if user_sign_in_request.password == manager.password:
                return True, "manager", manager.manager_id, manager.restaurant_id

        else:
            return False, "", -1

    def user_sign_up(self, db: Session, user_sign_up_request: UserSignUpRequest):
        email_already_used_in_customer = db.query(models.Customer).filter(
            func.lower(models.Customer.email) == user_sign_up_request.email.lower()).first()
        email_already_used_in_staff = db.query(models.Staff).filter(
            func.lower(models.Staff.email) == user_sign_up_request.email.lower()).first()
        email_already_used_in_manager = db.query(models.Manager).filter(
            func.lower(models.Manager.email) == user_sign_up_request.email.lower()).first()
        print(email_already_used_in_manager)
        if email_already_used_in_customer is not None or email_already_used_in_staff is not None or email_already_used_in_manager is not None:
            return "Email already exists!", False
        try:
            new_customer = models.Customer(email=user_sign_up_request.email, password=user_sign_up_request.password,
                                           phone_nb=user_sign_up_request.phone_nb,
                                           first_name=user_sign_up_request.first_name,
                                           last_name=user_sign_up_request.last_name,
                                           date_of_birth=user_sign_up_request.date_of_birth,
                                           picture="")
            db.add(new_customer)
            db.commit()
        except Exception as e:
            raise UserSignUpException(additional_message=e.__str__())
        return new_customer.customer_id, True

    def upload_profile_image(self, db: Session, user_id: Integer, image: UploadFile):
        image_destination = os.path.join(os.getcwd(), self.path_service.paths.users_images_path, f"img{user_id}.png")
        print(image_destination)
        print(os.path.exists(image_destination))
        if os.path.exists(image_destination):
            os.remove(image_destination)
        save_image(image, image_destination)
        user = db.query(models.Customer).filter_by(customer_id=user_id).first()
        user.picture = image_destination
        db.commit()

        to_return = db.query(models.Customer).filter_by(customer_id=user_id).first()
        to_return.picture = load_image(to_return.picture)
        return to_return

    def get_all_users(self, db: Session):
        data = db.query(models.Customer).all()
        return data

    def review_restaurant(self, db: Session, review_restaurant_request: ReviewRestaurantRequest):
        classes_inferred: dict = start_inference(review_comment=review_restaurant_request.comment)

        new_review = models.Review(restaurant_id=review_restaurant_request.restaurant_id,
                                   customer_id=review_restaurant_request.customer_id,
                                   rating=review_restaurant_request.rating, comment=review_restaurant_request.comment,
                                   classes=classes_inferred)
        db.add(new_review)
        db.commit()
        print(new_review.review_id)
        return db.query(models.Review).filter_by(restaurant_id=review_restaurant_request.restaurant_id).all()

    def reserve_table(self, db: Session, reserve_table_request: ReserveTableRequest):
        new_reservation = models.Reservation(table_id=reserve_table_request.table_id,
                                             customer_id=reserve_table_request.customer_id,
                                             reservation_time=reserve_table_request.time)
        db.add(new_reservation)
        db.commit()
        print(new_reservation.reservation_id)
        return new_reservation

    def get_all_bookings(self, db: Session, user_id: int):
        current_time = datetime.datetime.now()
        to_return: dict = {
            "passed_bookings": [],
            "upcoming_bookings": []
        }
        bookings = db.query(models.Reservation).filter_by(customer_id=user_id).all()
        for booking in bookings:
            table_id = booking.table_id
            booking_date = booking.reservation_time
            restaurant = db.query(models.Table).filter_by(table_id=table_id).first().restaurant
            restaurant_images = load_image(restaurant.images[0] if len(restaurant.images) > 0 else [])

            review_rate = get_restaurant_review_rate(restaurant)
            restaurant = restaurant.__dict__
            restaurant["review_rate"] = review_rate
            restaurant["images"] = restaurant_images
            booking_to_append = {
                "restaurant": restaurant,
                "table_id": table_id,
                "booking_date": booking_date.strftime('%m/%d/%Y - %H:%M')
            }

            if booking_date < current_time:
                to_return["passed_bookings"].append(booking_to_append)
            else:
                to_return["upcoming_bookings"].append(booking_to_append)

        return to_return
