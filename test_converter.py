import unittest

from converter import Converter


class ConverterTests(unittest.TestCase):
    def test_100_7(self):
        self.assertEqual(Converter.do(100.7), 1000)

    def test_100_8(self):
        self.assertEqual(Converter.do(100.8), 1000)

    def test_big_positive(self):
        self.assertEqual(Converter.do(99999.9), 1000)

    def test_100_6(self):
        self.assertEqual(Converter.do(100.6), 100)

    def test_0_1(self):
        self.assertEqual(Converter.do(0.1), 0)

    def test_1_0(self):
        self.assertEqual(Converter.do(1.0), 1)

    def test_65_7(self):
        self.assertEqual(Converter.do(65.7), 65)

    def test_50_1(self):
        self.assertEqual(Converter.do(50.1), 50)

    def test_zero(self):
        with self.assertRaises(ValueError):
            Converter.do(0.0)

    def test_minus_zero(self):
        with self.assertRaises(ValueError):
            Converter.do(-0.0)

    def test_minus_0_1(self):
        self.assertEqual(Converter.do(-0.1), -5)

    def test_minus_1_0(self):
        self.assertEqual(Converter.do(-1.0), -6)

    def test_minus_12_7(self):
        self.assertEqual(Converter.do(-12.7), -17)

    def test_minus_30_0(self):
        self.assertEqual(Converter.do(-30.0), -35)

    def test_minus_30_4(self):
        self.assertEqual(Converter.do(-30.4), -35)

    def test_minus_30_5(self):
        self.assertEqual(Converter.do(-30.5), -2000)

    def test_minus_30_6(self):
        self.assertEqual(Converter.do(-30.6), -2000)

    def test_minus_94_5(self):
        self.assertEqual(Converter.do(-94.5), -2000)

    def test_big_negative(self):
        self.assertEqual(Converter.do(-99999.9), -2000)

    def test_result_is_int(self):
        for x in (150.0, 65.7, -12.7, -50.0):
            self.assertIsInstance(Converter.do(x), int)

if __name__ == "__main__":
    unittest.main()