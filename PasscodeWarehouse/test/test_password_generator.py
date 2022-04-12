import unittest

from PasscodeWarehouse import password_generator


class MyTestCase(unittest.TestCase):
    def test_given_specific_rules_then_generate_expected_password(self):
        for i in range(10):
            pwd = password_generator.generate_password(lowercase=True, uppercase=False, number=True, custom_chars="",
                                                       required_length=8)
            self.assertEqual(8, len(pwd))
            self.assertTrue(pwd.islower())
            self.assertTrue(pwd.isalnum())

            pwd = password_generator.generate_password(lowercase=True, uppercase=True, number=False, custom_chars="@$",
                                                       required_length=6)
            self.assertEqual(6, len(pwd))
            self.assertTrue('@' in pwd or '$' in pwd)
            for character in pwd:
                self.assertTrue(character.islower() or character.isupper() or character == "@" or character == "$")


if __name__ == '__main__':
    unittest.main()
