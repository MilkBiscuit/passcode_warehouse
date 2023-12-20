from domain.model.credential_item import CredentialItem


# Informal Interfaces
# https://realpython.com/python-interface/#informal-interfaces
class ICredentialRepo:
    clear_text_dict: dict[str, CredentialItem] = {}
    cipher_text_dict: dict = {}

    def save(self, website: str, username: str, clear_text_pwd: str):
        pass

    def save_batch(self, clear_text_pwd_dict: dict[str: CredentialItem]):
        pass
