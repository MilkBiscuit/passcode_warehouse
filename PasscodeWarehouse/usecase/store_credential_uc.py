from PasscodeWarehouse.adapter.local_file_credential_repo import LocalFileCredentialRepo


def invoke(website: str, username: str, password: str):
    LocalFileCredentialRepo().save(website, username, password)
