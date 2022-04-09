import secrets
from base64 import urlsafe_b64encode as b64e, urlsafe_b64decode as b64d

from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

backend = default_backend()
DEFAULT_ITERATION_NUM = 10_000
# TODO: Should let user input the master password
MASTER_PASSWORD = "123456"


def _derive_key(pwd: bytes, salt: bytes, iteration_num: int = DEFAULT_ITERATION_NUM) -> bytes:
    # Derive a secret key from a given password and salt
    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt,
                     iterations=iteration_num, backend=backend)
    return b64e(kdf.derive(pwd))


def password_encrypt(msg: bytes, pwd: str, iteration_num: int = DEFAULT_ITERATION_NUM) -> bytes:
    salt = secrets.token_bytes(16)
    key = _derive_key(pwd.encode(), salt, iteration_num)
    return b64e(
        b'%b%b%b' % (
            salt,
            iteration_num.to_bytes(4, 'big'),
            b64d(Fernet(key).encrypt(msg))
        )
    )


def password_decrypt(token_bytes: bytes, pwd: str) -> bytes:
    decoded = b64d(token_bytes)
    salt, iteration_num, token_bytes = decoded[:16], decoded[16:20], b64e(decoded[20:])
    iterations = int.from_bytes(iteration_num, 'big')
    key = _derive_key(pwd.encode(), salt, iterations)
    return Fernet(key).decrypt(token_bytes)
