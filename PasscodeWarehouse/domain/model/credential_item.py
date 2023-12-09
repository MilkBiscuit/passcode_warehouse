from dataclasses import dataclass


@dataclass
class EncryptedCredentialItem:
    """Class for storing credentials into persistent storage."""
    id: str
    username: str
    encryptedPassword: str


@dataclass
class CredentialItem:
    id: str
    username: str
    password: str
