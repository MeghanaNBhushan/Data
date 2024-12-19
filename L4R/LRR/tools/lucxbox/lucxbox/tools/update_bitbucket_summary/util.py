import json
import typing
import jsonschema


def validate_json(schema_file: str, data: dict) -> None:
    """ Validate JSON data against provided schema file
    """
    with open(schema_file, 'r') as schf:
        schema = json.load(schf)
    jsonschema.validate(instance=data, schema=schema)


def read_json_file(file_name: str, schema_file: typing.Optional[str] = None) -> dict:
    """ Read JSON file and validate if schema_file parameter is provided
        Raises:
            jsonschema.exceptions.ValidationError
    """
    with open(file_name, 'r') as rfile:
        data = json.load(rfile)
    if schema_file:
        validate_json(schema_file, data)
    return data


def write_json_file(file_name: str, data: dict) -> None:
    """ Write data to JSON formatted file
    """
    with open(file_name, 'w') as outfile:
        outfile.write(json.dumps(data))
