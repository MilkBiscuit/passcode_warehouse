import json
from os.path import exists


CLEAR_TEXT_PWD_FILE_NAME = "clear_text_password.json"


def read():
    try:
        if exists(CLEAR_TEXT_PWD_FILE_NAME):
            with open(CLEAR_TEXT_PWD_FILE_NAME, "r") as reading_file:
                return json.load(reading_file)
    except Exception as e:
        print("Error when reading file:", e)


def write_into_file(data: dict):
    with open(CLEAR_TEXT_PWD_FILE_NAME, "w") as writing_file:
        json.dump(data, writing_file, indent=4)


