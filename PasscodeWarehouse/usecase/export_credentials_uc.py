import json
import typing

from PasscodeWarehouse.adapter.local_file_credential_repo import LocalFileCredentialRepo
from PasscodeWarehouse.domain import cryptography_related
from PasscodeWarehouse.domain.model.credential_item import EncryptedCredentialItem


def invoke(writing_file: typing.IO, master_password: str):
    encrypted_credentials: [str, EncryptedCredentialItem] = cryptography_related.encrypt_password_fields(
        LocalFileCredentialRepo().clear_text_dict, master_password
    )
    json.dump(encrypted_credentials, writing_file, indent=4, default=lambda __o: __o.__dict__)
    writing_file.close()
