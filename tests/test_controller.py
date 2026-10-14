import logging
import unittest
from unittest.mock import MagicMock, Mock, patch

from src.controller import Controller
from src.database import Database
from src.notifier import EmailSender, ResultSender
from src.triangle import Triangle
from src.user_interface import ConsoleUserInterface, UserInterface

def setUpModule():
    logging.disable(logging.CRITICAL)

def tearDownModule():
    logging.disable(logging.NOTSET)

class TestController(unittest.TestCase):

    def setUp(self):
        self.database = Database(":memory:")
        self.calculator = MagicMock(wraps=Triangle())
        self.user_interface = Mock(spec=UserInterface)
        self.sender = Mock(spec=ResultSender)
        self.controller = Controller(
            self.user_interface,
            self.database,
            self.calculator,
            self.sender
        )

    def tearDown(self):
        self.database.close()

    def user_enters(self, a_str, b_str, c_str):
        self.user_interface.get_sides.return_value = (a_str, b_str, c_str)

    def test_new_sides_are_calculated_and_saved_to_database(self):
        self.user_enters("3", "4", "5")

        result = self.controller.run()

        self.assertEqual(self.database.get("3", "4", "5"), ("разносторонний", ""))
        self.assertIn("разносторонний", result)

    def test_result_is_sent_to_third_party_dependency(self):
        self.user_enters("3", "4", "5")

        result = self.controller.run()

        self.sender.send.assert_called_once_with(result)

    def test_second_request_takes_result_from_database(self):
        self.user_enters("5", "5", "5")

        first_result = self.controller.run()
        second_result = self.controller.run()

        self.assertEqual(first_result, second_result)
        self.assertEqual(self.calculator.classify_triangle.call_count, 1)
        self.assertEqual(self.sender.send.call_count, 2)

    def test_result_is_calculated_again_after_record_was_deleted(self):
        self.user_enters("5", "5", "8")

        self.controller.run()
        self.database.delete("5", "5", "8")
        self.controller.run()

        self.assertEqual(self.calculator.classify_triangle.call_count, 2)

    def test_error_is_saved_for_sides_that_are_not_a_triangle(self):
        for sides in [("1", "2", "10"), ("-3", "4", "5"), ("0", "4", "5"), ("inf", "4", "5")]:
            with self.subTest(sides=sides):
                self.user_enters(*sides)

                result = self.controller.run()

                self.assertEqual(
                    self.database.get(*sides),
                    ("не треугольник", "стороны не образуют треугольник")
                )
                self.assertIn("стороны не образуют треугольник", result)

    def test_error_is_saved_for_non_numeric_sides(self):
        self.user_enters("abc", "4", "5")

        result = self.controller.run()

        self.assertEqual(self.database.get("abc", "4", "5"), ("", "нечисловые данные"))
        self.assertIn("нечисловые данные", result)

    def test_every_type_of_triangle_is_saved_to_database(self):
        expected_types = {
            ("5", "5", "5"): "равносторонний",
            ("5", "5", "8"): "равнобедренный",
            ("3", "5", "5"): "равнобедренный",
            ("3.5", "4.5", "5.5"): "разносторонний"
        }

        for sides, expected_type in expected_types.items():
            with self.subTest(sides=sides):
                self.user_enters(*sides)

                self.controller.run()

                self.assertEqual(self.database.get(*sides), (expected_type, ""))


class TestFullScenario(unittest.TestCase):

    @patch.object(EmailSender, "send", return_value=True)
    @patch("builtins.input", side_effect=["6", "8", "10"])
    def test_scenario_works_with_real_classes_and_stubs(self, fake_input, fake_send):
        database = Database(":memory:")
        controller = Controller(
            ConsoleUserInterface(),
            database,
            Triangle(),
            EmailSender()
        )

        result = controller.run()

        self.assertEqual(fake_input.call_count, 3)
        fake_send.assert_called_once_with(result)
        self.assertEqual(database.get("6", "8", "10"), ("разносторонний", ""))
        database.close()

if __name__ == "__main__":
    unittest.main()
