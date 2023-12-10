import unittest

from PasscodeWarehouse.domain import cryptography_related


class MyTestCase(unittest.TestCase):
    def given_a_message_when_encrypt_then_decrypt_returns_the_original_message(self):
        password = 'MyP@ssw0rd'
        cipher_text = cryptography_related.password_encrypt("Hello World", password)
        print("encrypted text is " + cipher_text)
        decoded_message = cryptography_related.password_decrypt(cipher_text, password)
        self.assertEqual("Hello World", decoded_message)

    def given_a_message_and_password_when_encrypt_twice_then_cipher_text_are_different(self):
        password = '123456'
        message = 'Hello'
        cipher_text_1 = cryptography_related.password_encrypt(message, password)
        cipher_text_2 = cryptography_related.password_encrypt(message, password)
        print("encrypted text 1st time: " + cipher_text_1)
        print("encrypted text 2nd time: " + cipher_text_2)
        # Can NOT use ECB
        self.assertNotEqual(cipher_text_1, cipher_text_2)


if __name__ == '__main__':
    unittest.main()
