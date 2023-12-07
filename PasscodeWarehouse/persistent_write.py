import json
import os
import typing
from os.path import exists

import persistent_read
from PasscodeWarehouse.domain import cryptography_related
from persistent_constants import *


def save(website: str, username: str, password: str):
    backup_passcode = persistent_read.read_user_backup_passcode()
    encrypted_pwd_str = cryptography_related.password_encrypt(password, backup_passcode)
    _save(website, username, encrypted_pwd_str, CLEAR_TEXT_PWD_FILE_NAME)


def save_user_backup_passcode(passcode: str):
    encrypted_username = cryptography_related.password_encrypt(
        PASSCODE_WAREHOUSE_USERNAME, PWD_TO_ENCRYPT_BACKUP_PASSCODE
    )
    encrypted_pwd = cryptography_related.password_encrypt(passcode, PWD_TO_ENCRYPT_BACKUP_PASSCODE)
    _save(PASSCODE_WAREHOUSE, encrypted_username, encrypted_pwd, BACKUP_PASSCODE_FILE_NAME)


def export_credentials(writing_file: typing.IO):
    data = persistent_read.read(CLEAR_TEXT_PWD_FILE_NAME)
    json.dump(data, writing_file, indent=4)
    writing_file.close()


def clear_all_credentials():
    if exists(CLEAR_TEXT_PWD_FILE_NAME):
        os.remove(CLEAR_TEXT_PWD_FILE_NAME)


def _save(website: str, username: str, encrypted_pwd_str: str, file_name: str):
    item_data = {
        website: {
            "username": username,
            "password": encrypted_pwd_str,
        }
    }
    try:
        if exists(file_name):
            existing_dict: dict = persistent_read.read(file_name)
            existing_keys = existing_dict.keys()
            for key in existing_keys:
                if key.lower() == website.lower():
                    existing_dict[key]["username"] = username
                    existing_dict[key]["password"] = encrypted_pwd_str
                    _write_into_file(existing_dict, file_name)

                    return

            existing_dict.update(item_data)
            _write_into_file(existing_dict, file_name)
        else:
            _write_into_file(item_data, file_name)
    except Exception as e:
        print("Error when saving into file:", e)


def _write_into_file(data: dict, file_name: str):
    with open(file_name, "w") as writing_file:
        json.dump(data, writing_file, indent=4)
