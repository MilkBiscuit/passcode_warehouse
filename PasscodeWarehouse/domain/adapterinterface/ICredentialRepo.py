from abc import ABC, abstractmethod

from domain.model.credential_item import CredentialItem


# Formal Interfaces
# https://realpython.com/python-interface/#formal-interfaces
class ICredentialRepo(ABC):
    clear_text_dict: dict[str, CredentialItem] = {}
    cipher_text_dict: dict = {}

    @abstractmethod
    def save(self, website: str, username: str, clear_text_pwd: str):
        pass

    @abstractmethod
    def save_batch(self, clear_text_pwd_dict: dict[str: CredentialItem]):
        pass
