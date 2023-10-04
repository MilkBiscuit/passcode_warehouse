import secrets
from base64 import urlsafe_b64encode as b64e, urlsafe_b64decode as b64d

from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

backend = default_backend()
DEFAULT_ITERATION_NUM = 10_000


def password_encrypt(msg: str, pwd: str, iteration_num: int = DEFAULT_ITERATION_NUM) -> str:
    encrypted_msg_bytes = _password_encrypt(msg.encode(), pwd, iteration_num)
    print("encrypted string is " + encrypted_msg_bytes.decode())

    return encrypted_msg_bytes.decode()


def password_decrypt(encrypted_msg: str, pwd: str) -> str:
    decrypted_bytes = _password_decrypt(encrypted_msg.encode(), pwd)

    return decrypted_bytes.decode()


def _derive_key(pwd: bytes, salt: bytes, iteration_num: int) -> bytes:
    # Derive a secret key from a given password and salt
    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt,
                     iterations=iteration_num, backend=backend)
    return b64e(kdf.derive(pwd))


def _password_encrypt(msg: bytes, pwd: str, iteration_num: int) -> bytes:
    salt = secrets.token_bytes(16)
    key = _derive_key(pwd.encode(), salt, iteration_num)
    print("iteration_num is " + b64e(b'%b' % iteration_num.to_bytes(4, 'big')).decode())
    print("salt is " + b64e(b'%b' % salt).decode())
    return b64e(
        b'%b%b%b' % (
            salt,
            iteration_num.to_bytes(4, 'big'),
            b64d(Fernet(key).encrypt(msg))
        )
    )


def _password_decrypt(token_bytes: bytes, pwd: str) -> bytes:
    decoded = b64d(token_bytes)
    salt, iteration_num, token_bytes = decoded[:16], decoded[16:20], b64e(decoded[20:])
    iterations = int.from_bytes(iteration_num, 'big')
    key = _derive_key(pwd.encode(), salt, iterations)
    return Fernet(key).decrypt(token_bytes)
