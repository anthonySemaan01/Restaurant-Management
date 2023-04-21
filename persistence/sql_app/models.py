from enum import Enum as PyEnum

from sqlalchemy import Column, ForeignKey, Integer, String, Enum, JSON, DateTime, Text, Numeric, LargeBinary
from sqlalchemy.orm import relationship

from persistence.sql_app.database import Base


class Manager(Base):
    __tablename__ = 'Manager'

    manager_id = Column(Integer, primary_key=True, autoincrement=True)
    restaurant_id = Column(Integer, ForeignKey('Restaurant.restaurant_id'), nullable=False)
    email = Column(String(255), nullable=False)
    password = Column(String(255), nullable=False)
    phone_nb = Column(String(255), nullable=False)
    first_name = Column(String(255), nullable=False)
    last_name = Column(String(255), nullable=False)
    date_of_birth = Column(DateTime, nullable=False)
    picture = Column(String(255))

    restaurant = relationship('Restaurant', back_populates='managers')
    reservations = relationship("Reservation", secondary="manager_reservation", back_populates="managers")
    orders = relationship("Order", secondary="manager_order", back_populates="managers")
    staffs = relationship("Staff", back_populates="manager")


class Customer(Base):
    __tablename__ = 'Customer'

    customer_id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(255), nullable=False)
    password = Column(String(255), nullable=False)
    phone_nb = Column(String(20), nullable=False)
    first_name = Column(String(255), nullable=False)
    last_name = Column(String(255), nullable=False)
    picture = Column(String(255))
    date_of_birth = Column(DateTime, nullable=False)

    reservations = relationship('Reservation', back_populates='customer')
    reviews = relationship('Review', back_populates='customer')


class Restaurant(Base):
    __tablename__ = 'Restaurant'

    restaurant_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    address = Column(String(255), nullable=False)
    phone_number = Column(String(255), nullable=False)

    cuisine = Column(JSON)
    website = Column(String(255))
    social_media_pages = Column(JSON)
    hours_of_operation = Column(String(255))
    dimensions = Column(JSON)
    images = Column(JSON)

    managers = relationship('Manager', back_populates='restaurant')
    staffs = relationship('Staff', back_populates='restaurant')
    tables = relationship('Table', back_populates='restaurant')
    reviews = relationship('Review', back_populates='restaurant')
    dishes = relationship('Dish', back_populates='restaurant')


class Staff(Base):
    __tablename__ = 'Staff'

    staff_id = Column(Integer, primary_key=True, autoincrement=True)
    manager_id = Column(Integer, ForeignKey('Manager.manager_id'))
    restaurant_id = Column(Integer, ForeignKey('Restaurant.restaurant_id'))
    email = Column(String(255), nullable=False)
    password = Column(String(255), nullable=False)
    phone_nb = Column(String(255), nullable=False)
    first_name = Column(String(255), nullable=False)
    last_name = Column(String(255), nullable=False)
    date_of_birth = Column(DateTime, nullable=False)
    picture = Column(String(255))

    restaurant = relationship('Restaurant', back_populates='staffs')
    reservations = relationship("Reservation", secondary="staff_reservation", back_populates="staffs")
    orders = relationship("Order", secondary="staff_order", back_populates="staffs")
    manager = relationship("Manager", back_populates="staffs")


class Order(Base):
    __tablename__ = 'Order'

    order_id = Column(Integer, primary_key=True, autoincrement=True)
    table_id = Column(Integer, ForeignKey('Table.table_id'), nullable=False)
    id_init = Column(Integer, ForeignKey('Staff.staff_id'), nullable=False)
    id_fin = Column(Integer, ForeignKey('Staff.staff_id'), nullable=False)
    status = Column(Enum('In Progress', 'Completed', 'Canceled'), nullable=False)
    time_init = Column(DateTime, nullable=False)
    time_fin = Column(DateTime)
    edits_made = Column(JSON)
    proc_type = Column(String(255))
    fin_type = Column(String(255))

    table = relationship('Table', back_populates='orders')
    staffs = relationship("Staff", secondary="staff_order", back_populates="orders")
    dishes = relationship("Dish", secondary="order_dish", back_populates="orders")
    managers = relationship("Manager", secondary="manager_order", back_populates="orders")


class Dish(Base):
    __tablename__ = 'Dish'

    dish_id = Column(Integer, primary_key=True, autoincrement=True)
    restaurant_id = Column(Integer, ForeignKey('Restaurant.restaurant_id'), nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(String(255), nullable=False)
    price = Column(Numeric(10, 2), nullable=False)
    picture = Column(String(255))

    restaurant = relationship('Restaurant', back_populates='dishes')
    orders = relationship("Order", secondary="order_dish", back_populates="dishes")


class ReservationStatus(PyEnum):
    PENDING = 'Pending'
    CONFIRMED = 'Confirmed'
    CANCELED_BY_CUSTOMER = 'Canceled by Customer'
    CANCELED_BY_RESTAURANT = 'Canceled by Restaurant'


class Reservation(Base):
    __tablename__ = 'Reservation'
    reservation_id = Column(Integer, primary_key=True, autoincrement=True)
    table_id = Column(Integer, ForeignKey('Table.table_id'), nullable=False)
    customer_id = Column(Integer, ForeignKey('Customer.customer_id'), nullable=False)
    id_proc = Column(Integer, ForeignKey('Staff.staff_id'), nullable=False)
    reservation_time = Column(DateTime, nullable=False)
    status = Column(Enum(ReservationStatus), nullable=False)
    proc_type = Column(String(255))

    customer = relationship("Customer", back_populates="reservations")
    staffs = relationship("Staff", secondary="staff_reservation", back_populates="reservations")
    managers = relationship("Manager", secondary="manager_reservation", back_populates="reservations")
    tables = relationship("Table", secondary="table_reservation", back_populates="reservations")


class Table(Base):
    __tablename__ = 'Table'
    table_id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    restaurant_id = Column(Integer, ForeignKey('Restaurant.restaurant_id'), nullable=False)
    capacity = Column(Integer, nullable=False)
    location = Column(JSON, nullable=False)

    restaurant = relationship('Restaurant', back_populates='tables')
    orders = relationship('Order', back_populates='table')

    reservations = relationship("Reservation", secondary="table_reservation", back_populates="tables")


class Review(Base):
    __tablename__ = 'Review'
    review_id = Column(Integer, primary_key=True, autoincrement=True)
    restaurant_id = Column(Integer, ForeignKey('Restaurant.restaurant_id'), nullable=False)
    customer_id = Column(Integer, ForeignKey('Customer.customer_id'), nullable=False)
    rating = Column(Integer, nullable=False)
    comment = Column(Text)
    restaurant = relationship('Restaurant', back_populates='reviews')
    customer = relationship('Customer', back_populates='reviews')


###########################################################################
class StaffReservation(Base):
    __tablename__ = 'staff_reservation'
    staff_id = Column(Integer, ForeignKey('Staff.staff_id'), primary_key=True)
    reservation_id = Column(Integer, ForeignKey('Reservation.reservation_id'), primary_key=True)


class ManagerReservation(Base):
    __tablename__ = 'manager_reservation'
    manager_id = Column(Integer, ForeignKey('Manager.manager_id'), primary_key=True)
    reservation_id = Column(Integer, ForeignKey('Reservation.reservation_id'), primary_key=True)


class ReservationTable(Base):
    __tablename__ = 'table_reservation'
    table_id = Column(Integer, ForeignKey('Table.table_id'), primary_key=True)
    reservation_id = Column(Integer, ForeignKey('Reservation.reservation_id'), primary_key=True)


class StaffOrder(Base):
    __tablename__ = 'staff_order'
    staff_id = Column(Integer, ForeignKey('Staff.staff_id'), primary_key=True)
    order_id = Column(Integer, ForeignKey('Order.order_id'), primary_key=True)


class ManagerOrder(Base):
    __tablename__ = 'manager_order'
    manager_id = Column(Integer, ForeignKey('Manager.manager_id'), primary_key=True)
    order_id = Column(Integer, ForeignKey('Order.order_id'), primary_key=True)


class OrderDish(Base):
    __tablename__ = 'order_dish'
    dish_id = Column(Integer, ForeignKey('Dish.dish_id'), primary_key=True)
    order_id = Column(Integer, ForeignKey('Order.order_id'), primary_key=True)
