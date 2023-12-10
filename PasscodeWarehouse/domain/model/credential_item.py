from dataclasses import dataclass


@dataclass
class EncryptedCredentialItem:
    """Class for storing credentials into persistent storage."""
    id: str
    username: str
    encryptedPassword: str

    def __getitem__(self, key):
        self.__dict__.__getitem__(key)


@dataclass
class CredentialItem:
    id: str
    username: str
    password: str
