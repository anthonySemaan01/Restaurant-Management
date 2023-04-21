from fastapi import APIRouter, UploadFile, Depends, File
from persistence.sql_app.db_dependency import get_db
from sqlalchemy.orm import Session
from containers import Services
from persistence.repositories.api_response import ApiResponse
from domain.contracts.services.abstract_restaurant_management import AbstractRestaurantManagement
from dependency_injector.wiring import inject, Provide
from domain.models.add_restaurant_request import AddRestaurantRequest, AddRestaurantImagesRequest
from domain.models.add_dishes_request import AddDishesRequest, DishUploadImage
from typing import List

router = APIRouter()


@router.get("/get_all")
@inject
async def get_all_users(db: Session = Depends(get_db), restaurant_management: AbstractRestaurantManagement = Depends(
    Provide[Services.restaurant_management])):
    return restaurant_management.get_all_restaurants(db)


@router.get("/get_by_id")
@inject
async def get_all_users(restaurant_id: int, db: Session = Depends(get_db),
                        restaurant_management: AbstractRestaurantManagement = Depends(
                            Provide[Services.restaurant_management])):
    return restaurant_management.get_restaurant_by_id(db=db, restaurant_id=restaurant_id)


@router.post("/add")
@inject
async def add_restaurant(add_restaurant_request: AddRestaurantRequest, db: Session = Depends(get_db),
                         restaurant_management: AbstractRestaurantManagement = Depends(
                             Provide[Services.restaurant_management])):
    return restaurant_management.add_restaurant(db=db, add_restaurant_request=add_restaurant_request)


@router.post("/add_images")
@inject
async def add_images_restaurant(add_restaurant_images_request: AddRestaurantImagesRequest = Depends(),
                                images: List[UploadFile] = File(...), db: Session = Depends(get_db),
                                restaurant_management: AbstractRestaurantManagement = Depends(
                                    Provide[Services.restaurant_management])):
    return restaurant_management.add_images_restaurant(db=db,
                                                       restaurant_id=add_restaurant_images_request.restaurant_id,
                                                       images=images)


@router.post("/add_dishes")
@inject
async def add_dishes(add_dishes_request: AddDishesRequest,
                     db: Session = Depends(get_db),
                     restaurant_management: AbstractRestaurantManagement = Depends(
                         Provide[Services.restaurant_management])):
    return restaurant_management.add_dishes(db=db, add_dishes_request=add_dishes_request)


@router.post("/add_dish_image")
@inject
async def add_dish_image(image: UploadFile, dish_id: DishUploadImage = Depends(),
                         db: Session = Depends(get_db),
                         restaurant_management: AbstractRestaurantManagement = Depends(
                             Provide[Services.restaurant_management])):
    return restaurant_management.upload_dish_image(db=db, dish_id=dish_id.dish_id, image=image)
