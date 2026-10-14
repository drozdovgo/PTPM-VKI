import logging
import unittest
from unittest.mock import patch

from src.notifier import EmailSender, ResultSender
from src.user_interface import ConsoleUserInterface, UserInterface


def setUpModule():
    logging.disable(logging.CRITICAL)


def tearDownModule():
    logging.disable(logging.NOTSET)


class TestInterfaces(unittest.TestCase):

    def test_user_interface_cannot_be_created_without_implementation(self):
        with self.assertRaises(TypeError):
            UserInterface()

    def test_result_sender_cannot_be_created_without_implementation(self):
        with self.assertRaises(TypeError):
            ResultSender()


class TestImplementations(unittest.TestCase):

    @patch("builtins.input", side_effect=["3", "4", "5"])
    def test_console_interface_reads_three_sides_from_input(self, fake_input):
        sides = ConsoleUserInterface().get_sides()

        self.assertEqual(sides, ("3", "4", "5"))
        self.assertEqual(fake_input.call_count, 3)

    def test_email_sender_imitates_successful_sending(self):
        self.assertTrue(EmailSender().send("Стороны 3, 4, 5 -> разносторонний"))


if __name__ == "__main__":
    unittest.main()
