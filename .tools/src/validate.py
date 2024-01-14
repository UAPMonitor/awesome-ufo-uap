import json
import os
from jsonschema import validate
from jsonschema.exceptions import ValidationError


def load_schema(schema_file):
    with open(schema_file, "r") as file:
        return json.load(file)


def load_data(data_file):
    with open(data_file, "r") as file:
        return json.load(file)


def validate_data(data, schema):
    try:
        validate(instance=data, schema=schema)
        return True, ""
    except ValidationError as e:
        return False, str(e)


def main():
    # Load configuration
    with open("config.json", "r") as file:
        config = json.load(file)

    schemas_dir = "schemas/latest"
    data_dir = config["data_dir"]

    for resource in config["resources"]:
        schema_file = os.path.join(schemas_dir, resource["ref"] + ".json")
        data_file = os.path.join(data_dir, resource["ref"] + ".json")

        if not os.path.exists(schema_file):
            print(f"Schema file not found: {schema_file}")
            continue

        if not os.path.exists(data_file):
            print(f"Data file not found: {data_file}")
            continue

        schema = load_schema(schema_file)
        data = load_data(data_file)

        is_valid, error_message = validate_data(data, schema)

        if is_valid:
            print(f"Validation successful for {data_file}")
        else:
            print(f"Validation failed for {data_file}: {error_message}")


if __name__ == "__main__":
    main()
