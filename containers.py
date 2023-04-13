from dependency_injector import containers, providers

from domain.contracts.services.abstract_user_management import AbstractUserManagement
from application.user_management.user_management import UserManagement

from domain.contracts.services.abstract_table_detection import AbstractTableDetection
from application.table_detection.table_detection import TableDetection


class Services(containers.DeclarativeContainer):
    # services
    user_management = providers.Factory(AbstractUserManagement.register(UserManagement))

    table_detection = providers.Factory(AbstractTableDetection.register(TableDetection))
