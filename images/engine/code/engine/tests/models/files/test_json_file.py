import json

from engine.models.files.json_file import JsonFile


def test_initial_content_is_json(create, file_path):
    json_file = create(JsonFile, file_path)
    initial_content = json_file._get_initial_content()
    assert isinstance(json.loads(initial_content), dict)
