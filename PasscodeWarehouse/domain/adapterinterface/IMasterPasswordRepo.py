from abc import ABC, abstractmethod


# Formal Interfaces
# https://realpython.com/python-interface/#formal-interfaces
class IMasterPasswordRepo(ABC):
    user_master_password: str = ""

    @abstractmethod
    def save_master_password(self, passcode: str):
        pass

    @abstractmethod
    def read_master_password(self) -> str:
        pass
