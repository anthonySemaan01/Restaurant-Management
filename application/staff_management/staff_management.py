import datetime
import os

from fastapi import UploadFile
from sqlalchemy.orm import Session

import persistence.sql_app.models as models
from domain.contracts.repositories.abstract_path_service import AbstractPathService
from domain.contracts.services.abstract_staff_management import AbstractStaffManagement
from domain.exceptions.staff_exception import StaffSignUpException
from domain.models.send_order_request import SendOrderRequest
from domain.models.staff_sign_in_request import StaffSignInRequest
from domain.models.staff_sign_up_request import StaffSignUpRequest
from shared.helpers.image_handler import load_image, save_image


class StaffManagement(AbstractStaffManagement):
    def __init__(self, path_service: AbstractPathService):
        self.path_service = path_service

    def get_all_staff(self, db: Session):
        data = db.query(models.Staff).all()
        return data

    def get_staff_by_id(self, db: Session, staff_id: int):
        staff = db.query(models.Staff).filter_by(staff_id=staff_id).first()
        if staff.picture:
            staff.picture = load_image(staff.picture)
        return staff

    def staff_sign_in(self, db: Session, staff_sign_in_request: StaffSignInRequest):
        staff = db.query(models.Staff).filter_by(email=staff_sign_in_request.email).first()

        if staff is not None:
            if staff_sign_in_request.password == staff.password:
                return True, staff.customer_id

        return False, -1

    def staff_sign_up(self, db: Session, staff_sign_up_request: StaffSignUpRequest):
        email_already_used_in_customer = db.query(models.Customer).filter_by(email=staff_sign_up_request.email).first()
        email_already_used_in_staff = db.query(models.Staff).filter_by(email=staff_sign_up_request.email).first()
        email_already_used_in_manager = db.query(models.Manager).filter_by(email=staff_sign_up_request.email).first()
        if email_already_used_in_customer is not None or email_already_used_in_staff is not None or email_already_used_in_manager is not None:
            return "Email already exists!", False
        try:
            new_staff = models.Staff(email=staff_sign_up_request.email, password=staff_sign_up_request.password,
                                     phone_nb=staff_sign_up_request.phone_nb,
                                     first_name=staff_sign_up_request.first_name,
                                     last_name=staff_sign_up_request.last_name,
                                     date_of_birth=staff_sign_up_request.date_of_birth,
                                     picture="")
            db.add(new_staff)
            db.commit()
        except Exception as e:
            raise StaffSignUpException(additional_message=e.__str__())
        return new_staff.staff_id, True

    def upload_profile_image(self, db: Session, staff_id: int, image: UploadFile):
        image_destination = os.path.join(os.getcwd(), self.path_service.paths.staffs_images_path, f"img{staff_id}.png")

        if os.path.exists(image_destination):
            os.remove(image_destination)
        save_image(image, image_destination)
        staff = db.query(models.Staff).filter_by(staff_id=staff_id).first()
        staff.picture = image_destination
        db.commit()

        to_return = db.query(models.Staff).filter_by(staff_id=staff_id).first()
        to_return.picture = load_image(to_return.picture)
        return to_return

    def get_bookings(self, db: Session, restaurant_id: int):
        current_time = datetime.datetime.now()
        to_return: dict = {
            "passed_bookings": [],
            "upcoming_bookings": []
        }
        tables = db.query(models.Table).filter_by(restaurant_id=restaurant_id).all()
        tables_ids: list = [table.table_id for table in tables]
        reservations = db.query(models.Reservation).filter(
            models.Reservation.table_id.in_(tables_ids)).all()

        for reservation in reservations:
            customer = db.query(models.Customer).filter_by(customer_id=reservation.customer_id).first().__dict__
            customer["picture"] = load_image(customer["picture"])
            booking_to_append = {
                "customer": customer,
                "table_id": reservation.table_id,
                "booking_date": reservation.reservation_time.strftime('%m/%d/%Y - %H:%M')
            }

            if reservation.reservation_time < current_time:
                to_return["passed_bookings"].append(booking_to_append)
            else:
                to_return["upcoming_bookings"].append(booking_to_append)

        return to_return

    def send_order(self, db: Session, send_order_request: SendOrderRequest):
        tables = db.query(models.Table).filter_by(restaurant_id=send_order_request.restaurant_id).all()
        tables_id = [table.table_id for table in tables]
        if send_order_request.table_id not in tables_id:
            return "Incorrect table ID", False
        dishes_ordered: list = list(send_order_request.dishes)
        to_store = []
        for dish in dishes_ordered:
            to_store.append({
                "dish_id": dish.dish_id,
                "count": dish.count
            })
        order = models.Order(table_id=send_order_request.table_id, dishes_ordered=to_store)
        db.add(order)
        db.commit()

        print(order.order_id)
        return order, True
