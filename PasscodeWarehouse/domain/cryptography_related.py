import base64

import rncryptor

cryptor = rncryptor.RNCryptor()


class PasswordDoesNotMatch(Exception):
    """Raised when the password does not match and fails to decrypt"""
    pass


def encrypt_password_fields(records: dict, master_pwd: str) -> dict:
    encrypted_records = {}
    for key, value in records.items():
        clear_text_pwd = value["password"]
        encrypted_pwd = password_encrypt(clear_text_pwd, master_pwd)
        encrypted_records[key] = {
            "username": value["username"],
            "encryptedPassword": encrypted_pwd
        }
    return encrypted_records


def decrypt_password_fields(encrypted_records: dict, master_pwd: str) -> dict:
    decrypted_result = {}
    for key, value in encrypted_records.items():
        decrypted_pwd = password_decrypt(value["encryptedPassword"], master_pwd)
        decrypted_result[key] = {
            "username": value["username"],
            "password": decrypted_pwd
        }
    return decrypted_result


def password_encrypt(msg: str, pwd: str) -> str:
    encrypted_msg_bytes = cryptor.encrypt(msg, pwd)
    encode_bytes = base64.encodebytes(encrypted_msg_bytes)
    encoded_string = encode_bytes.decode('utf-8')
    print(encode_bytes)
    print(encoded_string)

    return encoded_string


def password_decrypt(encrypted_msg: str, pwd: str) -> str:
    try:
        decrypted_bytes = encrypted_msg.encode('utf-8')
        decrypted_bytes = base64.decodebytes(decrypted_bytes)
        print(list(decrypted_bytes))
        decrypted_string = rncryptor.decrypt(decrypted_bytes, pwd)
        print(decrypted_string)

        return decrypted_string
    except Exception as e:
        print("password_decrypt error: ", e)
        raise PasswordDoesNotMatch
