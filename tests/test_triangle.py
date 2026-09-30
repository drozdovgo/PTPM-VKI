import unittest
from src.triangle import classify_triangle

class TestTriangle(unittest.TestCase):

    def test_equilateral(self):
        kind, points = classify_triangle("5", "5", "5")
        self.assertEqual(kind, "равносторонний")

    def test_isosceles_first_second(self):
        kind, points = classify_triangle("5", "5", "8")
        self.assertEqual(kind, "равнобедренный")

    def test_isosceles_second_third(self):
        kind, points = classify_triangle("3", "5", "5")
        self.assertEqual(kind, "равнобедренный")

    def test_scalene(self):
        kind, points = classify_triangle("3", "4", "5")
        self.assertEqual(kind, "разносторонний")

    def test_right_triangle(self):
        kind, points = classify_triangle("6", "8", "10")
        self.assertEqual(kind, "разносторонний")

    def test_float_sides(self):
        kind, points = classify_triangle("3.5", "4.5", "5.5")
        self.assertEqual(kind, "разносторонний")

    def test_inequality_large_side(self):
        kind, points = classify_triangle("1", "2", "10")
        self.assertEqual(kind, "не треугольник")

    def test_inequality_equal_sum(self):
        kind, points = classify_triangle("1", "2", "3")
        self.assertEqual(kind, "не треугольник")

    def test_negative_side(self):
        kind, points = classify_triangle("-3", "4", "5")
        self.assertEqual(kind, "не треугольник")

    def test_zero_side(self):
        kind, points = classify_triangle("0", "4", "5")
        self.assertEqual(kind, "не треугольник")

    def test_string_letters(self):
        kind, points = classify_triangle("abc", "4", "5")
        self.assertEqual(kind, "")

    def test_string_spaces(self):
        kind, points = classify_triangle(" ", "4", "5")
        self.assertEqual(kind, "")

    def test_empty_string(self):
        kind, points = classify_triangle("", "4", "5")
        self.assertEqual(kind, "")

    def test_none_input(self):
        with self.assertRaises(TypeError):
            classify_triangle(None, "4", "5")

    def test_list_input(self):
        with self.assertRaises(TypeError):
            classify_triangle(["3"], "4", "5")

    def test_points_length(self):
        kind, points = classify_triangle("3", "4", "5")
        self.assertEqual(len(points), 3)

    def test_points_are_tuples(self):
        kind, points = classify_triangle("5", "5", "5")
        for point in points:
            self.assertIsInstance(point, tuple)

    def test_points_not_error_state(self):
        kind, points = classify_triangle("3", "4", "5")
        self.assertNotEqual(points, [(-1, -1), (-1, -1), (-1, -1)])

    def test_points_is_error_state(self):
        kind, points = classify_triangle("-1", "4", "5")
        self.assertEqual(points, [(-1, -1), (-1, -1), (-1, -1)])

    def test_large_valid_triangle(self):
        kind, points = classify_triangle("100", "100", "100")
        self.assertEqual(kind, "равносторонний")
        self.assertEqual(len(points), 3)

if __name__ == '__main__':
    unittest.main()