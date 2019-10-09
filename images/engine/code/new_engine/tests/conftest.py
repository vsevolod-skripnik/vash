from new_engine.models.file import File
from new_engine.models.folder import Folder
from new_engine.models.resource import Resource
from new_engine.models.resources.page import Page
from new_engine.models.resources.template import Template

NODE_SUBCLUSSES = [File, Folder, Resource, Template, Page]

NODE_PATHS = [
    '/tmp/the-holy-grail/french-castle/trojan-badger',
    '/tmp/the-holy-grail/the-black-knight',
]

RESOURCE_PATHS_SETS = [
    ['tests/the-holy-grail/french-castle/trojan-badger', 'tests/the-holy-grail/the-black-knight'],
    ['tests/the-black-knight'],
]
