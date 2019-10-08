from new_engine.logger import logger
from new_engine.models.resource import Resource
from new_engine.models.file import File
from new_engine.models.folder import Folder


class Template(Resource):
    @property
    def root_folder(self):
        return '/resources/templates'

    def _get_files(self):
        return {
            'meta': File(f'{self.path}/{self.name}.json'),
        }
