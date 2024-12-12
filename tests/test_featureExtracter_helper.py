import unittest
from featureExtracter_helper import (
    add_numbers,
    multiply_numbers,
    divide_numbers,
    concatenate_strings,
    reverse_string,
    # is_palindrome  # This function will not be tested
)


class TestFeatureExtracterHelper(unittest.TestCase):
    def test_add_numbers(self):
        self.assertEqual(add_numbers(2, 3), 5)
        self.assertEqual(add_numbers(-1, 1), 0)
        self.assertEqual(add_numbers(0, 0), 0)

    def test_multiply_numbers(self):
        self.assertEqual(multiply_numbers(2, 3), 6)
        self.assertEqual(multiply_numbers(-1, 2), -2)
        self.assertEqual(multiply_numbers(0, 5), 0)

    def test_divide_numbers(self):
        self.assertEqual(divide_numbers(6, 3), 2)
        self.assertIsNone(divide_numbers(5, 0))
        self.assertEqual(divide_numbers(0, 1), 0)

    def test_concatenate_strings(self):
        self.assertEqual(concatenate_strings("hello", " world"), "hello world")
        self.assertEqual(concatenate_strings("", "test"), "test")
        self.assertEqual(concatenate_strings("foo", ""), "foo")

    def test_reverse_string(self):
        self.assertEqual(reverse_string("hello"), "olleh")
        self.assertEqual(reverse_string("world"), "dlrow")
        self.assertEqual(reverse_string(""), "")

    # Note: The `is_palindrome` function is intentionally not tested.


if __name__ == "__main__":
    unittest.main()
