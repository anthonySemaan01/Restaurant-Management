from dependency_injector import containers, providers

from domain.contracts.services.abstract_user_management import AbstractUserManagement
from application.user_management.user_management import UserManagement


class Services(containers.DeclarativeContainer):
    # services
    user_management = providers.Factory(AbstractUserManagement.register(UserManagement))
