import json
import re
import typing
from os.path import exists

import cryptography_related
import persistent_write
from persistent_constants import *

user_backup_passcode = ""


def read(file_name: str) -> dict:
    try:
        if exists(file_name):
            with open(file_name, "r") as reading_file:
                return json.load(reading_file)
        return {}
    except Exception as e:
        print("Error when reading file:", e)
        return {}


def read_user_backup_passcode() -> str:
    global user_backup_passcode
    if user_backup_passcode != "":
        return user_backup_passcode

    matched_result = _search_matched_results(PASSCODE_WAREHOUSE, read(BACKUP_PASSCODE_FILE_NAME))
    matched_num = len(matched_result.keys())
    if matched_num == 1:
        if PASSCODE_WAREHOUSE_USERNAME == cryptography_related.password_decrypt(
                matched_result[PASSCODE_WAREHOUSE]["username"], PWD_TO_ENCRYPT_BACKUP_PASSCODE
        ):
            user_backup_passcode = cryptography_related.password_decrypt(
                matched_result[PASSCODE_WAREHOUSE]["password"], PWD_TO_ENCRYPT_BACKUP_PASSCODE
            )

            return user_backup_passcode
        else:
            print("Decryption of backup passcode failed.")
    else:
        print("Expect backup passcode num: 1, but actual num:", matched_num)
    user_backup_passcode = ""
    return user_backup_passcode


def import_credentials(reading_file: typing.IO, passcode: str) -> Exception | None:
    try:
        imported_dictionary = json.load(reading_file)
        decrypted_credentials = _decrypt_password_fields(imported_dictionary, passcode)
        no_backup_passcode = False
        if read_user_backup_passcode() == "":
            persistent_write.save_user_backup_passcode(passcode)
            no_backup_passcode = True

        for key, value in decrypted_credentials.items():
            persistent_write.save(key, value["username"], value["password"])

        if no_backup_passcode:
            return RuntimeWarning(no_backup_passcode)
        else:
            return None
    except Exception as e:
        print("exception", e)

        return e


def search_and_decrypt(website_keyword: str) -> dict:
    if read_user_backup_passcode() == "":
        return {}

    results = _search_matched_results(website_keyword, read(CLEAR_TEXT_PWD_FILE_NAME))
    return _decrypt_password_fields(results, user_backup_passcode)


# Returns a dictionary with encrypted text directly
def _search_matched_results(website_keyword: str, dictionary: dict) -> dict:
    result = {}

    for key in dictionary.keys():
        if re.search(website_keyword, key, re.IGNORECASE):
            result[key] = {
                "username": dictionary[key]["username"],
                "password": dictionary[key]["password"]
            }

    return result


def _decrypt_password_fields(encrypted_records: dict, decrypt_passcode: str) -> dict:
    decrypted_result = {}
    for key, value in encrypted_records.items():
        decrypted_pwd = cryptography_related.password_decrypt(value["password"], decrypt_passcode)
        decrypted_result[key] = {
            "username": encrypted_records[key]["username"],
            "password": decrypted_pwd
        }
    return decrypted_result
