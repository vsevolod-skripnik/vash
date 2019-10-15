import pytest

from engine.models.files.file import File
from engine.models.files.json_file import JsonFile
from engine.models.files.meta_file import MetaFile
from engine.models.files.page_meta_file import PageMetaFile
from engine.models.files.template_meta_file import TemplateMetaFile
from engine.models.folder import Folder
from engine.models.resource import Resource
from engine.models.resources.page import Page
from engine.models.resources.template import Template

NODE_SUBCLUSSES = [File, Folder, Resource, Template, Page]

FILE_AND_SUBCLUSSES = [File, JsonFile, MetaFile, PageMetaFile, TemplateMetaFile]
RESOURCE_AND_SUBCLUSSES = [Resource, Page, Template]

NODE_PATHS = [
    '/tmp/the-holy-grail/french-castle/trojan-badger',
    '/tmp/the-holy-grail/the-black-knight',
]

RESOURCE_PATHS = [
    'tests/the-holy-grail/french-castle/trojan-badger',
    'tests/the-holy-grail/the-black-knight',
]
RESOURCE_NEW_PATHS = RESOURCE_PATHS[::-1]


RESOURCE_PATHS_SETS = [
    ['tests/the-holy-grail/french-castle/trojan-badger', 'tests/the-holy-grail/the-black-knight'],
    ['tests/the-black-knight'],
]


@pytest.fixture
def create():
    call_history = []

    def _create(model, *args, **kwargs):
        instance = model(*args, **kwargs)
        instance.create()
        call_history.append(
            {
                'instance': instance,
                'model': model,
                'args': args,
                'kwargs': kwargs
            }
        )
        return instance

    yield _create

    for record in call_history:
        record['instance'].delete()

        # If test moves instance to another place, delete previous place
        instance = record['model'](*record['args'], **record['kwargs'])
        instance.delete()


@pytest.fixture(params=NODE_PATHS)
def node_path(request):
    return request.param


@pytest.fixture(params=RESOURCE_PATHS)
def resource_path(request):
    return request.param


@pytest.fixture(params=RESOURCE_NEW_PATHS)
def resource_new_path(request):
    return request.param


file_path = node_path
folder_path = node_path
