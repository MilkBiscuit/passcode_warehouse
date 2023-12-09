import os
from os.path import exists

from PasscodeWarehouse.adapter.master_password_repo import MasterPasswordRepo
from PasscodeWarehouse.domain.model.credential_item import CredentialItem
from PasscodeWarehouse.sensitive_data import DEFAULT_MASTER_PASSWORD
from PasscodeWarehouse.util import persistent_helper
from PasscodeWarehouse.domain import cryptography_related

PWD_FILE_NAME = "clear_text_password.json"


class LocalFileCredentialRepo:
    _instance = None
    clear_text_dict: dict[str, CredentialItem] = {}

    def __new__(cls, *args, **kw):
        if cls._instance is None:
            cls._instance = object.__new__(cls)
            cls._instance._load_master_password()
            cls._instance._load_all_credentials()
        return cls._instance

    def __init__(self):
        pass

    def clear_all_credentials(self):
        if exists(PWD_FILE_NAME):
            os.remove(PWD_FILE_NAME)
            self.clear_text_dict = {}

    def save(self, website: str, username: str, password: str) -> bool:
        item = CredentialItem(id=website, username=username, password=password)
        self.clear_text_dict[website] = item
        encrypted_dict = cryptography_related.encrypt_password_fields(self.clear_text_dict, self.master_password)
        persistent_helper.write_dict(encrypted_dict, PWD_FILE_NAME)
        return True

    def _load_all_credentials(self):
        if exists(PWD_FILE_NAME):
            encrypted_credentials = persistent_helper.read_dict(PWD_FILE_NAME)
            self.clear_text_dict = cryptography_related.decrypt_password_fields(
                encrypted_credentials, self.master_password
            )

    def _load_master_password(self):
        saved_master_password = MasterPasswordRepo().read_master_password()
        if saved_master_password == "":
            self.master_password = DEFAULT_MASTER_PASSWORD
        else:
            self.master_password = saved_master_password
