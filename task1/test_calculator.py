import unittest
from calculator import add, sub, mul, div

class TestArithmetic(unittest.TestCase):

    # 1. Звичайні тести
    def test_add(self):
        self.assertEqual(add(5, 3), 8)

    def test_sub(self):
        self.assertEqual(sub(10, 4), 6)

    def test_mul(self):
        self.assertEqual(mul(2, 7), 14)

    def test_div(self):
        self.assertEqual(div(8, 2), 4)

    # 2. Тести з перевіркою виключень
    def test_div_zero(self):
        with self.assertRaises(ZeroDivisionError):
            div(10, 0)

    # 3. Параметризовані тести через subTest
    def test_add_parametrized(self):
        test_cases = [
            (1, 1, 2),
            (-5, 3, -2),
            (10, 0, 10),
        ]

        for a, b, expected in test_cases:
            with self.subTest(a=a, b=b, expected=expected):
                self.assertEqual(add(a, b), expected)

    def test_mul_parametrized(self):
        test_cases = [
            (2, 3, 6),
            (-1, 5, -5),
            (0, 100, 0),
        ]

        for a, b, expected in test_cases:
            with self.subTest(a=a, b=b, expected=expected):
                self.assertEqual(mul(a, b), expected)

    def test_div_parametrized(self):
        test_cases = [
            (10, 2, 5),
            (9, 3, 3),
            (-12, -3, 4),
        ]

        for a, b, expected in test_cases:
            with self.subTest(a=a, b=b, expected=expected):
                self.assertEqual(div(a, b), expected)


if __name__ == '__main__':
    unittest.main()
