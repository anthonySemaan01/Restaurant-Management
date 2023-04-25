from dependency_injector import containers, providers

from application.manager_management.manager_management import ManagerManagement
from application.restaurant_management.restaurant_management import RestaurantManagement
from application.staff_management.staff_management import StaffManagement
from application.table_detection.table_detection import TableDetection
from application.user_management.user_management import UserManagement
from domain.contracts.repositories.abstract_path_service import AbstractPathService
from domain.contracts.services.abstract_manager_management import AbstractManagerManagement
from domain.contracts.services.abstract_restaurant_management import AbstractRestaurantManagement
from domain.contracts.services.abstract_staff_management import AbstractStaffManagement
from domain.contracts.services.abstract_table_detection import AbstractTableDetection
from domain.contracts.services.abstract_user_management import AbstractUserManagement
from persistence.services.path_service import PathService


class Services(containers.DeclarativeContainer):
    # services
    paths_service = providers.Singleton(AbstractPathService.register(PathService))

    user_management = providers.Singleton(AbstractUserManagement.register(UserManagement), path_service=paths_service)

    table_detection = providers.Singleton(AbstractTableDetection.register(TableDetection), path_service=paths_service)

    restaurant_management = providers.Singleton(AbstractRestaurantManagement.register(RestaurantManagement),
                                                path_service=paths_service)

    staff_management = providers.Singleton(AbstractStaffManagement.register(StaffManagement),
                                           path_service=paths_service)

    manager_management = providers.Singleton(AbstractManagerManagement.register(ManagerManagement),
                                             path_service=paths_service)
