import json
import logging
import typing
from enum import Enum, auto

from PasscodeWarehouse.adapter.local_file_credential_repo import LocalFileCredentialRepo
from PasscodeWarehouse.domain.cryptography_related import *


class ImportResult(Enum):
    SUCCESS = auto()
    DECRYPT_PASSCODE_INCORRECT = auto()
    OTHER_ERROR = auto()


def invoke(reading_file: typing.IO, passcode: str) -> ImportResult:
    try:
        imported_array = json.load(reading_file)
        imported_dict: dict[str: dict] = {item["id"]: item for item in imported_array}
        logging.info("array is converted to dict.")
        decrypted_credentials: dict[str: CredentialItem] = decrypt_password_fields(imported_dict, passcode)
        logging.info("decryption complete.")
        LocalFileCredentialRepo().save_batch(decrypted_credentials)
        logging.info("save batch complete.")
        return ImportResult.SUCCESS
    except PasswordDoesNotMatch:
        return ImportResult.DECRYPT_PASSCODE_INCORRECT
    except Exception as e:
        logging.error(msg="Other exception when importing:", exc_info=e)
        return ImportResult.OTHER_ERROR
