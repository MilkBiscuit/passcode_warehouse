from PasscodeWarehouse.domain.adapterinterface import IMasterPasswordRepo
from PasscodeWarehouse.adapter.master_password_repo import MasterPasswordRepo

master_pwd_repo: IMasterPasswordRepo = MasterPasswordRepo()


def has_master_pwd() -> bool:
    return master_pwd_repo.read_master_password() == ""


def save_master_pwd(pwd: str):
    master_pwd_repo.save_master_password(passcode=pwd)
