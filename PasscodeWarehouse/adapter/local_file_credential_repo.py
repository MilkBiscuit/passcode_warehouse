import logging
import os
from os.path import exists

from PasscodeWarehouse.adapter.master_password_repo import MasterPasswordRepo
from PasscodeWarehouse.domain.model.credential_item import CredentialItem
from PasscodeWarehouse.sensitive_data import DEFAULT_MASTER_PASSWORD
from PasscodeWarehouse.util import persistent_helper
from PasscodeWarehouse.domain import cryptography_related

PWD_FILE_NAME = "clear_text_password.json"

logging.basicConfig(
    format="%(asctime)s.%(msecs)03d %(levelname)-8s %(message)s",
    level=logging.DEBUG,
    datefmt="%Y-%m-%d %H:%M:%S"
)


class LocalFileCredentialRepo:
    _instance = None
    clear_text_dict: dict[str, CredentialItem] = {}
    cipher_text_dict: dict = {}

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

    def save(self, website: str, username: str, clear_text_pwd: str):
        self._add_or_update(website, username, clear_text_pwd)
        persistent_helper.write_dict(self.cipher_text_dict, PWD_FILE_NAME)

    def save_batch(self, clear_text_password_dict: dict[str: CredentialItem]):
        for key, value in clear_text_password_dict.items():
            self._add_or_update(key, value.username, value.password)
        persistent_helper.write_dict(self.cipher_text_dict, PWD_FILE_NAME)

    def _add_or_update(self, website: str, username: str, clear_text_pwd: str):
        item = CredentialItem(id=website, username=username, password=clear_text_pwd)
        self.clear_text_dict[website] = item
        logging.info("Start to encrypt " + website)
        encrypted_password = cryptography_related.password_encrypt(clear_text_pwd, self.master_password)
        logging.info("Encryption completed for: " + website)
        self.cipher_text_dict[website] = {
            "id": website,
            "username": username,
            "encryptedPassword": encrypted_password
        }

    def _load_all_credentials(self):
        logging.debug("_load_all_credentials")
        if exists(PWD_FILE_NAME):
            self.cipher_text_dict = persistent_helper.read_dict(PWD_FILE_NAME)
            self.clear_text_dict = cryptography_related.decrypt_password_fields(
                self.cipher_text_dict, self.master_password
            )
        logging.debug("_load_all_credentials complete")

    def _load_master_password(self):
        logging.debug("_load_master_password")
        saved_master_password = MasterPasswordRepo().read_master_password()
        if saved_master_password == "":
            self.master_password = DEFAULT_MASTER_PASSWORD
        else:
            self.master_password = saved_master_password
