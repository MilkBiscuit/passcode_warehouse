import json
import typing
from enum import Enum, auto

from PasscodeWarehouse.adapter.local_file_credential_repo import LocalFileCredentialRepo
from PasscodeWarehouse.domain.cryptography_related import *


class ImportResult(Enum):
    SUCCESS = auto()
    INHERIT_BACKUP_PASSCODE = auto()
    DECRYPT_PASSCODE_INCORRECT = auto()
    OTHER_ERROR = auto()


def invoke(reading_file: typing.IO, passcode: str) -> ImportResult:
    try:
        imported_dictionary = json.load(reading_file)
        decrypted_credentials = decrypt_password_fields(imported_dictionary, passcode)
        for key, value in decrypted_credentials.items():
            website = key
            username = value["username"]
            password = value["password"]
            LocalFileCredentialRepo().save(website, username, password)
        # re_encrypted_credentials = encrypt_password_fields(decrypted_credentials, DEFAULT_MASTER_PASSWORD)
        # LocalFileCredentialRepo().existing_dict = re_encrypted_credentials
        return ImportResult.SUCCESS
        # no_backup_passcode = False
        # if read_user_backup_passcode() == "":
        #     persistent_write.save_user_backup_passcode(passcode)
        #     no_backup_passcode = True
    except PasswordDoesNotMatch:
        return ImportResult.DECRYPT_PASSCODE_INCORRECT
    except Exception as e:
        print("Other exception when importing:", e)
        return ImportResult.OTHER_ERROR
