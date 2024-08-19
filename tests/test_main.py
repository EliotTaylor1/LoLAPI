import unittest
from unittest.mock import patch, MagicMock

from src import main


class TestMain(unittest.TestCase):

    def test_is_account_name_valid(self):
        name = "Eiiot"
        self.assertTrue(main.is_account_name_valid(name))
        name = "E"
        self.assertFalse(main.is_account_name_valid(name))

    def test_is_tag_valid(self):
        tag = "EUW"
        self.assertTrue(main.is_tag_valid(tag))
        tag = "E UW"
        self.assertFalse(main.is_tag_valid(tag))


if __name__ == "__main__":
    unittest.main()
