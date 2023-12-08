from PasscodeWarehouse.domain import cryptography_related
from PasscodeWarehouse.sensitive_data import PASSCODE_WAREHOUSE_USERNAME, PWD_TO_ENCRYPT_BACKUP_PASSCODE, \
    PASSCODE_WAREHOUSE
from PasscodeWarehouse.util import persistent_helper

BACKUP_PASSCODE_FILE_NAME = "backup_passcode.json"


class MasterPasswordRepo:
    _instance = None
    user_master_password: str = ""

    def __new__(cls, *args, **kw):
        if cls._instance is None:
            cls._instance = object.__new__(cls)
            cls._instance.read_master_password()
        return cls._instance

    def __init__(self):
        pass

    def save_master_password(self, passcode: str):
        encrypted_username = cryptography_related.password_encrypt(
            PASSCODE_WAREHOUSE_USERNAME, PWD_TO_ENCRYPT_BACKUP_PASSCODE
        )
        encrypted_pwd = cryptography_related.password_encrypt(passcode, PWD_TO_ENCRYPT_BACKUP_PASSCODE)
        item = {
            PASSCODE_WAREHOUSE: {
                "username": encrypted_username,
                "password": encrypted_pwd
            }
        }
        persistent_helper.write_dict(item, BACKUP_PASSCODE_FILE_NAME)
        self.user_master_password = passcode

    def read_master_password(self) -> str:
        if self.user_master_password != "":
            return self.user_master_password

        read_result = persistent_helper.read_dict(BACKUP_PASSCODE_FILE_NAME)
        matched_num = len(read_result.keys())
        if matched_num == 1:
            if PASSCODE_WAREHOUSE_USERNAME == cryptography_related.password_decrypt(
                    read_result[PASSCODE_WAREHOUSE]["username"], PWD_TO_ENCRYPT_BACKUP_PASSCODE
            ):
                self.user_master_password = cryptography_related.password_decrypt(
                    read_result[PASSCODE_WAREHOUSE]["password"], PWD_TO_ENCRYPT_BACKUP_PASSCODE
                )

                return self.user_master_password
            else:
                print("Decryption of backup passcode failed.")
        else:
            print("Expect backup passcode num: 1, but actual num:", matched_num)
        self.user_master_password = ""
        return ""
