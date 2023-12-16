import json
import typing
from enum import Enum, auto

from PasscodeWarehouse.adapter.local_file_credential_repo import LocalFileCredentialRepo
from PasscodeWarehouse.domain.cryptography_related import *


class ImportResult(Enum):
    SUCCESS = auto()
    DECRYPT_PASSCODE_INCORRECT = auto()
    OTHER_ERROR = auto()


# TODO: fix the bug, when the app is in /Application folder, import doesn't always work
def invoke(reading_file: typing.IO, passcode: str) -> ImportResult:
    try:
        imported_array = json.load(reading_file)
        imported_dict: dict[str: dict] = {item["id"]: item for item in imported_array}
        decrypted_credentials: dict[str: CredentialItem] = decrypt_password_fields(imported_dict, passcode)
        LocalFileCredentialRepo().save_batch(decrypted_credentials)
        return ImportResult.SUCCESS
    except PasswordDoesNotMatch:
        return ImportResult.DECRYPT_PASSCODE_INCORRECT
    except Exception as e:
        print("Other exception when importing:", e)
        return ImportResult.OTHER_ERROR
