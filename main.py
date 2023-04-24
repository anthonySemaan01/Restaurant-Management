import uvicorn
from fastapi import FastAPI, File
from starlette.middleware.cors import CORSMiddleware
from api.controllers import health_check_controller, user_controller, table_detection_controller, restaurant_controller, \
    staff_controller, manager_controller
from persistence.sql_app.database import engine, SessionLocal
from persistence.sql_app import models
from containers import Services

app = FastAPI(version='1.0', title='Restaurant Management Backend',
              description="Providing different services")

services = Services()

services.wire(
    modules=[health_check_controller, user_controller, table_detection_controller, restaurant_controller,
             staff_controller, manager_controller])

models.Base.metadata.create_all(bind=engine)

app.add_middleware(CORSMiddleware,
                   allow_origins=["*"],
                   allow_credentials=True,
                   allow_methods=["*"],
                   allow_headers=["*"],
                   )

app.include_router(
    router=health_check_controller.router,
    prefix="/health",
    tags=["health"],
)

app.include_router(
    router=user_controller.router,
    prefix="/user",
    tags=["user"],
)

app.include_router(
    router=staff_controller.router,
    prefix="/staff",
    tags=["staff"],
)

app.include_router(
    router=manager_controller.router,
    prefix="/manager",
    tags=["manager"],
)

app.include_router(
    router=restaurant_controller.router,
    prefix="/restaurant",
    tags=["restaurant"],
)

app.include_router(
    router=table_detection_controller.router,
    prefix="/detection",
    tags=["table detection"],
)

if __name__ == '__main__':
    uvicorn.run('main:app', host="localhost", port=2000)
