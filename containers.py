from dependency_injector import containers, providers

from domain.contracts.services.abstract_user_management import AbstractUserManagement
from application.user_management.user_management import UserManagement

from domain.contracts.services.abstract_table_detection import AbstractTableDetection
from application.table_detection.table_detection import TableDetection

from domain.contracts.repositories.abstract_path_service import AbstractPathService
from persistence.services.path_service import PathService


class Services(containers.DeclarativeContainer):
    # services
    paths_service = providers.Singleton(AbstractPathService.register(PathService))

    user_management = providers.Singleton(AbstractUserManagement.register(UserManagement), path_service=paths_service)

    table_detection = providers.Singleton(AbstractTableDetection.register(TableDetection), path_service=paths_service)


