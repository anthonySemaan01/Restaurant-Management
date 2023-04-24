import os
import datetime
from domain.contracts.services.abstract_user_management import AbstractUserManagement
from sqlalchemy.orm import Session
import persistence.sql_app.models as models
from domain.models.review_restaurant_request import ReviewRestaurantRequest
from domain.models.reserve_table_request import ReserveTableRequest
from domain.models.user_sign_up_request import UserSignUpRequest
from domain.exceptions.user_exception import UserSignUpException
from domain.contracts.repositories.abstract_path_service import AbstractPathService
from fastapi import UploadFile, File
from sqlalchemy import Integer
from shared.helpers.image_handler import load_image, save_image
from domain.models.user_sign_in_request import UserSignInRequest
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
        customer = db.query(models.Customer).filter_by(email=user_sign_in_request.email).first()
        staff = db.query(models.Staff).filter_by(email=user_sign_in_request.email).first()
        manager = db.query(models.Manager).filter_by(email=user_sign_in_request.email).first()

        if customer is not None:
            if user_sign_in_request.password == customer.password:
                return True, "customer", customer.customer_id

        elif staff is not None:
            if user_sign_in_request.password == staff.password:
                return True, "staff", staff.staff_id

        elif manager is not None:
            if user_sign_in_request.password == manager.password:
                return True, "manager", manager.manager_id

        else:
            return False, "", -1

    def user_sign_up(self, db: Session, user_sign_up_request: UserSignUpRequest):
        try:
            new_customer = models.Customer(email=user_sign_up_request.email, password=user_sign_up_request.password,
                                           phone_nb=user_sign_up_request.password,
                                           first_name=user_sign_up_request.first_name,
                                           last_name=user_sign_up_request.last_name,
                                           date_of_birth=user_sign_up_request.date_of_birth)
            db.add(new_customer)
            db.commit()
        except Exception as e:
            raise UserSignUpException(additional_message=e.__str__())
        return new_customer.customer_id

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
        new_review = models.Review(restaurant_id=review_restaurant_request.restaurant_id,
                                   customer_id=review_restaurant_request.customer_id,
                                   rating=review_restaurant_request.rating, comment=review_restaurant_request.comment)
        db.add(new_review)
        db.commit()
        print(new_review.review_id)
        return new_review

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
