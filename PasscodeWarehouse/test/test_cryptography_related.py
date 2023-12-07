import unittest

from PasscodeWarehouse.domain import cryptography_related


class MyTestCase(unittest.TestCase):
    def test_given_a_message_when_encrypt_then_decrypt_returns_the_message(self):
        password = 'MyP@ssw0rd'
        token = cryptography_related.password_encrypt("Hello World", password)
        decoded_message = cryptography_related.password_decrypt(token, password)
        self.assertEqual("Hello World", decoded_message)  # add assertion here


if __name__ == '__main__':
    unittest.main()
