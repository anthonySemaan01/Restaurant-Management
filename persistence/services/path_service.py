import json

from domain.contracts.repositories.abstract_path_service import AbstractPathService
from domain.models.api_paths import ApiPaths


class PathService(AbstractPathService):
    def __init__(self):
        with open('assets/paths.json') as paths:
            self._paths: ApiPaths = ApiPaths.parse_obj(json.load(paths))

    @property
    def paths(self) -> ApiPaths:
        return self._paths
