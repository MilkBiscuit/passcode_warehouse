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
        json.dump(data, writing_file, indent=4)

# def save_user_backup_passcode(passcode: str):
#     encrypted_username = cryptography_related.password_encrypt(
#         PASSCODE_WAREHOUSE_USERNAME, PWD_TO_ENCRYPT_BACKUP_PASSCODE
#     )
#     encrypted_pwd = cryptography_related.password_encrypt(passcode, PWD_TO_ENCRYPT_BACKUP_PASSCODE)
#     _save(PASSCODE_WAREHOUSE, encrypted_username, encrypted_pwd, BACKUP_PASSCODE_FILE_NAME)


# def read_user_backup_passcode() -> str:
#     global user_backup_passcode
#     if user_backup_passcode != "":
#         return user_backup_passcode
#
#     matched_result = _search_matched_results(PASSCODE_WAREHOUSE, read(BACKUP_PASSCODE_FILE_NAME))
#     matched_num = len(matched_result.keys())
#     if matched_num == 1:
#         if PASSCODE_WAREHOUSE_USERNAME == cryptography_related.password_decrypt(
#                 matched_result[PASSCODE_WAREHOUSE]["username"], PWD_TO_ENCRYPT_BACKUP_PASSCODE
#         ):
#             user_backup_passcode = cryptography_related.password_decrypt(
#                 matched_result[PASSCODE_WAREHOUSE]["password"], PWD_TO_ENCRYPT_BACKUP_PASSCODE
#             )
#
#             return user_backup_passcode
#         else:
#             print("Decryption of backup passcode failed.")
#     else:
#         print("Expect backup passcode num: 1, but actual num:", matched_num)
#     user_backup_passcode = ""
#     return user_backup_passcode
