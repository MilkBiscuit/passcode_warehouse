

# Informal Interfaces
# https://realpython.com/python-interface/#informal-interfaces
class IMasterPasswordRepo:
    user_master_password: str = ""

    def save_master_password(self, passcode: str):
        pass

    def read_master_password(self) -> str:
        pass
