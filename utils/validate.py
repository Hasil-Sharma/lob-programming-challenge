import logging
from jsonschema import validate
import jsonschema

logger = logging.getLogger('Validation')

get_type_obj = lambda x: {"type": x}


def validate_config(conf_dict, key):
    if key == "auth":
        schema = {
            "type": "object",
            "properties": {
                "civic-key": get_type_obj("string"),
                "lob-key": get_type_obj("string")
            },
            "required": ["civic-key", "lob-key"]
        }
        try:
            validate(conf_dict, schema)
        except jsonschema.exceptions.ValidationError as e:
            logger.error("Error is authentication keys: %s", e.message)
            exit(1)
    elif key == "civic-api":
        schema = {
            "type": "object",
            "properties": {
                "url": get_type_obj("string"),
                "key": get_type_obj("string"),
                "fields": get_type_obj("string"),
                "levels": get_type_obj("array"),
                "roles": {
                    "type": "array",
                    "minItems": 1
                }
            }
        }
        try:
            validate(conf_dict, schema)
        except jsonschema.exceptions.ValidationError as e:
            logger.error("Error is civic-api configurations: %s", e.message)
            exit(1)
    elif key == "lob-api":
        schema = {
            "type": "object",
            "properties": {
                "file": get_type_obj("string"),
                "color": get_type_obj("bool"),
                "description": get_type_obj("string"),
                "html_variables": get_type_obj("array")
            }
        }
        try:
            validate(conf_dict, schema)
        except jsonschema.exceptions.ValidationError as e:
            logger.error("Error in lob-api configurations: %s", e.message)


def validate_input(input_dict):
    logger.info("Validating Input File")
    json_schema = {
        "type": "object",
        "properties": {
            "name": get_type_obj("string"),
            "address_line1": get_type_obj("string"),
            "address_line2": get_type_obj("string"),
            "address_city": get_type_obj("string"),
            "address_state": get_type_obj("string"),
            "address_zip": get_type_obj(["string", "integer"]),
            "html_variables": get_type_obj("object")
        },
        "required": ["name", "address_line1", "address_city", "address_state", "address_zip", "html_variables"]
    }
    try:
        validate(input_dict, json_schema)
    except jsonschema.exceptions.ValidationError as e:
        logger.error("Error in input specified: %s", e.message)
        exit(1)
