import unittest.mock
import json
import pytest
import jsonschema

import lucxbox.tools.update_bitbucket_summary.util as util

@pytest.fixture
def sample_json_schema():
    return '''{
      "$schema": "http://json-schema.org/draft-07/schema#",
      "title": "Test schema",
      "type": "object",
      "properties": {
        "int": {
          "type": "integer"
        }
      },
      "required": [
        "int"
      ]
    }'''


def test_validate_json_success(sample_json_schema):
    json_data = json.loads('{"int" : 1}')
    mock_open = unittest.mock.mock_open(read_data=sample_json_schema)
    with unittest.mock.patch('builtins.open', mock_open):
        assert util.validate_json('schema.json', json_data) is None


def test_validate_json_failure(sample_json_schema):
    json_data = json.loads('{"test" : "wrong"}')
    mock_open = unittest.mock.mock_open(read_data=sample_json_schema)
    with pytest.raises(jsonschema.exceptions.ValidationError):
        with unittest.mock.patch('builtins.open', mock_open):
            util.validate_json('schema.json', json_data)


def test_read_json(tmpdir):
    test_data = '{"int" : 1}'
    file = tmpdir.join('input.json')
    file.write(test_data)
    assert util.read_json_file(file) == json.loads(test_data)


def test_read_json_valid_schema(sample_json_schema, tmpdir):
    test_data = '{"int" : 1}'
    file = tmpdir.join('input.json')
    schema_file = tmpdir.join('schema.json')
    schema_file.write(sample_json_schema)
    file.write(test_data)
    assert util.read_json_file(file, schema_file) == json.loads(test_data)


def test_read_json_invalid_schema(sample_json_schema, tmpdir):
    test_data = '{"int" : "invalid"}'
    file = tmpdir.join('input.json')
    schema_file = tmpdir.join('schema.json')
    schema_file.write(sample_json_schema)
    file.write(test_data)
    with pytest.raises(jsonschema.exceptions.ValidationError):
        util.read_json_file(file, schema_file)


def test_write_json_file_success(tmpdir):
    file = tmpdir.join('output.json')
    test_data_string = '{"json": "valid"}'
    test_data = json.loads(test_data_string)
    util.write_json_file(file, test_data)
    assert file.read() == test_data_string
