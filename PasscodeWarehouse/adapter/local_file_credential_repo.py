import os
from os.path import exists

from PasscodeWarehouse.sensitive_data import DEFAULT_MASTER_PASSWORD
from PasscodeWarehouse.util import persistent_helper
from PasscodeWarehouse.domain import cryptography_related

PWD_FILE_NAME = "clear_text_password.json"


class LocalFileCredentialRepo:
    _instance = None
    clear_text_dict: dict = {}

    def __new__(cls, *args, **kw):
        if cls._instance is None:
            cls._instance = object.__new__(cls, *args, **kw)
            cls._instance._load_all_credentials()
        return cls._instance

    def __init__(self):
        pass

    def clear_all_credentials(self):
        if exists(PWD_FILE_NAME):
            os.remove(PWD_FILE_NAME)
            self.clear_text_dict = {}

    def save(self, website: str, username: str, password: str) -> bool:
        item_data = {
            "username": username,
            "password": password,
        }
        self.clear_text_dict[website] = item_data
        encrypted_dict = cryptography_related.encrypt_password_fields(self.clear_text_dict, DEFAULT_MASTER_PASSWORD)
        persistent_helper.write_dict(encrypted_dict, PWD_FILE_NAME)
        return True

    def _load_all_credentials(self):
        if exists(PWD_FILE_NAME):
            encrypted_credentials = persistent_helper.read_dict(PWD_FILE_NAME)
            self.clear_text_dict = cryptography_related.decrypt_password_fields(
                encrypted_credentials, DEFAULT_MASTER_PASSWORD
            )
