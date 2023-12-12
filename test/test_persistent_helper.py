import unittest
from dataclasses import dataclass
from io import StringIO

from PasscodeWarehouse.util import persistent_helper


@dataclass
class _Company:
    id: int
    name: str


@dataclass
class _User:
    id: int
    name: str
    email: str
    company: _Company


class MyTestCase(unittest.TestCase):
    def test_write_simple_dict_to_output(self):
        outfile = StringIO()
        persistent_helper.write_to_output(outfile=outfile, dict_content={
            "name": "Chandler"
        })
        outfile.seek(0)
        content = outfile.read()
        self.assertNotEqual(-1, content.find('"name": "Chandler"'))

    def test_write_object_to_output(self):
        example_company = _Company(id=555, name="Example Ltd")
        chocolate_company = _Company(id=1964, name="Charlie and the Chocolate Factory")
        user_1 = _User(id=1, name="John Doe", email="john@doe.net", company=example_company)
        user_2 = _User(id=2, name="Willy Wonka", email="willy.wonka@chocolatefactory.com", company=chocolate_company)
        dict_to_write = {
            "first": user_1,
            "second": user_2
        }
        outfile = StringIO()
        persistent_helper.write_to_output(outfile=outfile, dict_content=dict_to_write)
        outfile.seek(0)
        content = outfile.read()
        print(content)
        self.assertNotEqual(-1, content.find("Charlie and the Chocolate Factory"))
        self.assertNotEqual(-1, content.find("555"))


if __name__ == '__main__':
    unittest.main()
