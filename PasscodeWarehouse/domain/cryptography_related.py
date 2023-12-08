import base64

import rncryptor

DEFAULT_ITERATION_NUM = 10_000
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


def password_encrypt(msg: str, pwd: str, iteration_num: int = DEFAULT_ITERATION_NUM) -> str:
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

# def _derive_key(pwd: bytes, salt: bytes, iteration_num: int) -> bytes:
#     # Derive a secret key from a given password and salt
#     kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt,
#                      iterations=iteration_num, backend=backend)
#     return b64e(kdf.derive(pwd))


# def _password_encrypt(msg: bytes, pwd: str, iteration_num: int) -> bytes:
#     salt = secrets.token_bytes(16)
#     key = _derive_key(pwd.encode(), salt, iteration_num)
#     print("iteration_num is " + b64e(b'%b' % iteration_num.to_bytes(4, 'big')).decode())
#     print("salt is " + b64e(b'%b' % salt).decode())
#     return b64e(
#         b'%b%b%b' % (
#             salt,
#             iteration_num.to_bytes(4, 'big'),
#             b64d(Fernet(key).encrypt(msg))
#         )
#     )


# def _password_decrypt(token_bytes: bytes, pwd: str):
#     return rncryptor.decrypt(token_bytes, pwd)
# decoded = b64d(token_bytes)
# salt, iteration_num, token_bytes = decoded[:16], decoded[16:20], b64e(decoded[20:])
# iterations = int.from_bytes(iteration_num, 'big')
# key = _derive_key(pwd.encode(), salt, iterations)
# return Fernet(key).decrypt(token_bytes)
