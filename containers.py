from dependency_injector import containers, providers

from domain.contracts.services.abstract_user_management import AbstractUserManagement
from application.user_management.user_management import UserManagement

from domain.contracts.services.abstract_table_detection import AbstractTableDetection
from application.table_detection.table_detection import TableDetection

from domain.contracts.repositories.abstract_path_service import AbstractPathService
from persistence.services.path_service import PathService

from domain.contracts.services.abstract_restaurant_management import AbstractRestaurantManagement
from application.restaurant_management.restaurant_management import RestaurantManagement

from domain.contracts.services.abstract_staff_management import AbstractStaffManagement
from application.staff_management.staff_management import StaffManagement


class Services(containers.DeclarativeContainer):
    # services
    paths_service = providers.Singleton(AbstractPathService.register(PathService))

    user_management = providers.Singleton(AbstractUserManagement.register(UserManagement), path_service=paths_service)

    table_detection = providers.Singleton(AbstractTableDetection.register(TableDetection), path_service=paths_service)

    restaurant_management = providers.Singleton(AbstractRestaurantManagement.register(RestaurantManagement),
                                                path_service=paths_service)

    staff_management = providers.Singleton(AbstractStaffManagement.register(StaffManagement),
                                           paths_service=paths_service)
