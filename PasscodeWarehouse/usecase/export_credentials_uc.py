import json
import typing

from PasscodeWarehouse.adapter.local_file_credential_repo import LocalFileCredentialRepo
from PasscodeWarehouse.domain import cryptography_related


def invoke(writing_file: typing.IO, master_password: str):
    encrypted_credentials = cryptography_related.encrypt_password_fields(
        LocalFileCredentialRepo().clear_text_dict, master_password
    )
    json.dump(encrypted_credentials, writing_file, indent=4)
    writing_file.close()
