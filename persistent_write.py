import json
from os.path import exists

import persistent_read
from persistent_read import CLEAR_TEXT_PWD_FILE_NAME


def save(website: str, username: str, password: str):
    item_data = {
        website: {
            "username": username,
            "password": password,
        }
    }
    try:
        if exists(CLEAR_TEXT_PWD_FILE_NAME):
            existing_dict: dict = persistent_read.read()
            existing_keys = existing_dict.keys()
            for key in existing_keys:
                if key.lower() == website.lower():
                    existing_dict[key]["username"] = username
                    existing_dict[key]["password"] = password
                    write_into_file(existing_dict)

                    return

            existing_dict.update(item_data)
            write_into_file(existing_dict)
        else:
            write_into_file(item_data)
    except Exception as e:
        print("Error when saving into file:", e)


def write_into_file(data: dict):
    with open(CLEAR_TEXT_PWD_FILE_NAME, "w") as writing_file:
        json.dump(data, writing_file, indent=4)


