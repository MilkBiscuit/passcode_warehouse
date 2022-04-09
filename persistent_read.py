import json
import re
from os.path import exists

import cryptography_related

CLEAR_TEXT_PWD_FILE_NAME = "clear_text_password.json"
BACKUP_PASSCODE_FILE_NAME = "backup_passcode.json"
PASSCODE_WAREHOUSE = "Passcode Warehouse"
PASSCODE_WAREHOUSE_USERNAME = "NA"
PWD_TO_ENCRYPT_BACKUP_PASSCODE = "P@ssw0rd"
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

    matched_result = _search_matched_results(PASSCODE_WAREHOUSE, BACKUP_PASSCODE_FILE_NAME)
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


def search_matched_results(website_keyword: str) -> dict:
    if read_user_backup_passcode() == "":
        return {}

    results = _search_matched_results(website_keyword, CLEAR_TEXT_PWD_FILE_NAME)
    # filter_out_backup_passcode_results = {key: value for key, value in results.items() if key != PASSCODE_WAREHOUSE}
    decrypted_result = {}
    for key, value in results.items():
        decrypted_pwd = cryptography_related.password_decrypt(value["password"], user_backup_passcode)
        decrypted_result[key] = {
            "username": results[key]["username"],
            "password": decrypted_pwd
        }
    return decrypted_result


# Returns a dictionary with encrypted text directly
def _search_matched_results(website_keyword: str, file_name: str) -> dict:
    result = {}
    # if not exists(file_name):
    #     return result

    dictionary: dict = read(file_name)
    for key in dictionary.keys():
        if re.search(website_keyword, key, re.IGNORECASE):
            result[key] = {
                "username": dictionary[key]["username"],
                "password": dictionary[key]["password"]
            }

    return result
