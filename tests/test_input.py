import unittest

import src.inputs


class TestInput(unittest.TestCase):

    def test_is_account_name_valid(self):
        valid_names = ["Eiiot", "123456", "EEE", "àccents", "12AAaa56n", "space name"]
        invalid_names = ["", "aVeryLongNameeeeeeeeeee", "Ae"]
        for name in valid_names:
            with self.subTest(name=name):
                self.assertTrue(src.inputs.is_account_name_valid(name))
        for name in invalid_names:
            with self.subTest(name=name):
                self.assertFalse(src.inputs.is_account_name_valid(name))

    def test_is_tag_valid(self):
        valid_tags = ["EUW", "NA1", "YEAH", "yes", "àààa"]
        invalid_tags = ["#EUW", "TOOLONG", "A", "a"]
        for tag in valid_tags:
            with self.subTest(tag=tag):
                self.assertTrue(src.inputs.is_tag_valid(tag))
        for tag in invalid_tags:
            with self.subTest(tag=tag):
                self.assertFalse(src.inputs.is_tag_valid(tag))


if __name__ == "__main__":
    unittest.main()
