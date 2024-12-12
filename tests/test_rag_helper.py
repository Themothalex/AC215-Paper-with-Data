import unittest
from rag_helper import (
    generate_random_string,
    perform_number_operations,
    analyze_string,
    irrelevant_calculation,
    obscure_transformation,
)


class TestRagHelper(unittest.TestCase):
    def test_generate_random_string(self):
        result = generate_random_string(5)
        self.assertEqual(len(result), 5)
        self.assertTrue(all(c.isalnum() for c in result))
        self.assertEqual(generate_random_string(0), "")
        self.assertIsNone(generate_random_string(-1))

    def test_perform_number_operations(self):
        result = perform_number_operations(10, 5)
        self.assertEqual(result["addition"], 15)
        self.assertEqual(result["subtraction"], 5)
        self.assertEqual(result["multiplication"], 50)
        self.assertEqual(result["division"], 2)

        result = perform_number_operations(10, 0)
        self.assertIsNone(result["division"])
        self.assertIsNone(perform_number_operations("a", 5))

    def test_analyze_string(self):
        result = analyze_string("Hello123")
        self.assertEqual(result["vowel_count"], 2)
        self.assertEqual(result["consonant_count"], 3)
        self.assertEqual(result["digit_count"], 3)
        self.assertEqual(result["total_length"], 8)
        self.assertIsNone(analyze_string(123))

    def test_irrelevant_calculation(self):
        self.assertEqual(irrelevant_calculation(3), 13)
        self.assertEqual(irrelevant_calculation(0), 13)
        self.assertIsNone(irrelevant_calculation("string"))

    def test_obscure_transformation(self):
        result = obscure_transformation([1, 2, 3])
        self.assertEqual(result, [4, 7, 12])
        self.assertEqual(obscure_transformation([]), [])
        self.assertIsNone(obscure_transformation("not a list"))


if __name__ == "__main__":
    unittest.main()
