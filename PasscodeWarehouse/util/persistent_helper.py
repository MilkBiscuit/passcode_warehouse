import json
from os.path import exists


def read_dict(file_name: str) -> dict:
    try:
        if exists(file_name):
            with open(file_name, "r") as reading_file:
                return json.load(reading_file)
        return {}
    except Exception as e:
        print("Error when reading file:", e)
        return {}


def write_dict(data: dict, file_name: str):
    with open(file_name, "w") as writing_file:
        json.dump(data, writing_file, indent=4, default=lambda __o: __o.__dict__)
